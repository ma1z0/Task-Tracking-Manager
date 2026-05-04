from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "owner",
            "assignee",
            "due_date",
            "completed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "completed_at",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        current_user = self.context["request"].user
        task = self.instance

        if task is None:
            return attrs
        
        if current_user == task.owner:
            return attrs
        
        if current_user == task.assignee:
            allowed_fields = {"status"}
            incoming_fields = set(attrs.keys())
            forbidden_fields = incoming_fields - allowed_fields

            if forbidden_fields:
                raise serializers.ValidationError("Assignee can only update status")
            
            return attrs
    
        return attrs