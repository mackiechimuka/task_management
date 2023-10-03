from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer


class AdminTaskView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        data = request.data.copy()

        try:
            serializer = TaskSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            task = serializer.save(allocated_to_id=data['allocated_to'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except KeyError:
            return Response({'error': 'Invalid data. Missing allocated_to field.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RetrieveTaskView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TaskAllView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tasks = Task.objects.filter(allocated_to=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RetrieveAllTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, allocated_to=request.user)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
                return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, allocated_to=request.user)

            if 'completed' in request.data:
                completed = request.data['completed']
                task.completed = completed
                task.save()
                serializer = TaskSerializer(task)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid request. Missing completed field.'}, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)