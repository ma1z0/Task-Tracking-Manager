from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from tasks.models import Task
from tasks.serializers import TaskSerializer
from tasks.permissions import IsOwnerOrAssigneeLimited

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAssigneeLimited]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'updated_at', 'completed_at', 'status']
    ordering = ["-created_at"]
    
    def get_queryset(self):

        queryset = Task.objects.filter(
            Q(owner=self.request.user) | Q(assignee=self.request.user)
        ).distinct()

        task_status = self.request.query_params.get('status')
        if task_status:
            queryset = queryset.filter(status=task_status)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)