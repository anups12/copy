from django import forms
from . models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TaskCreate(forms.ModelForm): 
    class Meta:
        model = Task
        fields = ( 'title', 'description', 'due_date', 'status')

        widgets = {
        'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Add Title '}),
        'description': forms.Textarea(attrs={'class':'form-control', 'rows':3, 'placeholder':"Add description ..."}),
        'due_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        'status': forms.Select(attrs={'class':'form-control'}),
            
        }

class UserCreate(UserCreationForm):
    class Meta:
        model = User
        fields = ( 'first_name', 'username', 'email', 'password1', 'password2')
        widgets = {
        'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}),
        'first_name': forms.TextInput(attrs={'class':'form-control',  'placeholder':"Enter Name "}),
        'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}),
        'password1' : forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password '}),
        'password2': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter confirm password'}),
        }