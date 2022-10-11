from django.forms import ModelMultipleChoiceField
from rest_framework import serializers
from . models import  Task

class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'tags']

        qs = Task.objects.prefetch_related('tags')
        widget={
            'status': ModelMultipleChoiceField(qs)
        }