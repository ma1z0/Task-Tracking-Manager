from tasks.models import Task
from tasks.serializers import TaskSerializer
from rest_framework import viewsets

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self): 
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)