from django.contrib import admin
from . models import Task, UserProfile, Tag

# Register your models here.
@admin.register(Task)
class TaskRegister(admin.ModelAdmin):
    model = Task
    list_display= ('id','user','title', 'due_date', 'status',)
  

@admin.register(Tag)
class TagRegister(admin.ModelAdmin):
    model = Tag
    list_display= ('name','id')  

@admin.register(UserProfile)
class UserRegister(admin.ModelAdmin):
    model = UserProfile
    list_display= ('username', 'name', 'email')