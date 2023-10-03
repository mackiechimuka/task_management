from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    allocated_to = serializers.StringRelatedField()
    class Meta:
        model =Task
        fields =['id','title', 'description', 'allocated_to', 'due_date', 'completed']

    
    