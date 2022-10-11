from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True) 

    def __str__(self):
        return self.name

STATUS_CHOICES=(
    ('open','OPEN'),
    ('working','WORKING'),
    ('done','DONE'),
    ('overdue','OVERDUE'),
)
class Task(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    description=models.TextField(max_length=1000)
    due_date= models.DateField(blank=True, default=datetime.now())
    status = models.CharField(choices=STATUS_CHOICES, max_length=8, default='open')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def number_of_tags(self):
        return self.tags.all()

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.name

