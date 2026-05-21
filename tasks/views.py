from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(APIView):

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)

        is_completed = request.query_params.get("is_completed")
        priority = request.query_params.get("priority")
        due_date = request.query_params.get("due_date")
        search = request.query_params.get("search")
        ordering = request.query_params.get("ordering", "-created_at")

        if is_completed == "true":
            tasks = tasks.filter(is_completed=True)

        if is_completed == "false":
            tasks = tasks.filter(is_completed=False)

        if priority:
            tasks = tasks.filter(priority=priority.upper())

        if due_date:
            tasks = tasks.filter(due_date=due_date)

        if search:
            tasks = tasks.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        allowed_ordering = [
            "created_at", "-created_at",
            "due_date", "-due_date",
            "priority", "-priority",
            "title", "-title",
        ]

        if ordering in allowed_ordering:
            tasks = tasks.order_by(ordering)

        page = int(request.query_params.get("page", 1))
        limit = int(request.query_params.get("limit", 5))

        start = (page - 1) * limit
        end = start + limit

        total_tasks = tasks.count()

        serializer = TaskSerializer(tasks[start:end], many=True)

        return Response({
            "success": True,
            "total_tasks": total_tasks,
            "page": page,
            "limit": limit,
            "results": serializer.data
        })

    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "success": True,
                "message": "Task created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        serializer = TaskSerializer(task)
        return Response({
            "success": True,
            "data": serializer.data
        })

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "success": True,
                "message": "Task updated successfully",
                "data": serializer.data
            })

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "success": True,
                "message": "Task updated successfully",
                "data": serializer.data
            })

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.delete()
        return Response({
            "success": True,
            "message": "Task deleted successfully"
        })
    
