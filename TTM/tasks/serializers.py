from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "status", "owner", "assignee", "created_at", "updated_at", "due_date", "completed_at"]
        read_only_fields = ["owner", "created_at", "updated_at", "completed_at"]