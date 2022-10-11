from django.urls import path
from . import views 

urlpatterns = [
    path('', views.Home, name='home'),
    path('signin/', views.Create_User, name='signin'),
    path('login/', views.Login_User, name='login'),
    path('logout/', views.LogoutUser, name='logout'),
    path('edit_post/<int:pk>/', views.EditPost, name='edit_post'),
    path('delete_post/<int:pk>/', views.DeletePost, name='delete_post'),
    path('delete_tags/<int:pk>/', views.DeleteTags, name='delete_tags'),
    path('add_tags/', views.AddTags, name='add_tags'),


#     path('task_api/', views.TaskApi.as_view()),
#     path('task_api/<int:pk>/', views.TaskApi.as_view()),
#     path('country/', views.GetDropDownCountry, name='country'),
#     path('state/', views.GetState, name='state'),
#     path('city/', views.GetCity, name='city'),
]