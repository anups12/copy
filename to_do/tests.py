from django.test import TestCase
from . models import Task, Tag

# Create your tests here.

class TestModels(TestCase):
    def setUp(self) :
        self.tagss=Tag.objects.create( name='arun')
        self.tasks=Task.objects.create(title='New task')

    def test_task_model(self):
        task_data=Task.objects.last()
        self.assertEqual(task_data.title, 'New task')

    def test_no_of_tags(self):
        task_data=Task.objects.last()
        self.assertEqual(task_data.user, None)
