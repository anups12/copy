import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from . forms import TaskCreate, UserCreate
from . models import Task, UserProfile, Tag
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer
import datetime




# <------------------------Api View----------------------------->
class TaskApi(APIView):
    def get(self, request, pk=None, format=None):
        x=datetime.datetime.today().weekday()
        y=datetime.datetime.now().time().minute
        default=False
        if x=='Saturday' or x=='Sunday':
            default = True
        if y >=0 and y<8:
            default = True
# <----------------------GET DATA FROM THE DATABASE --------------->
        if pk is not None:
            try:
               
                task = Task.objects.get(id=pk)
                serializer = TaskSerializer(task)
                return Response(serializer.data)
            except:
                return Response({'message': "The data you are requesting is not available or deleted ", "default":default})
        else:       
            task = Task.objects.all()
            serializer=TaskSerializer(task, many=True)
            return Response(serializer.data )

# <----------------------To add data  (POST request) --------------->
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            tags=request.data.get('tags')
            for x in tags:
                if not Tag.objects.filter(name=x).exists():
                    Tag.objects.create(name=x)

            tag_id=[]
            for x in tags: 
                tag_id.append(int(Tag.objects.get(name=x).id))
            serializer.save(tags=tag_id)
            
            return Response({'message':'Your data has been added successfully '})
        return Response(serializer.errors)

# <----------------------FOR COMPLETE DATA UPDATE --------------->
    def put(self, request,pk, format=None):
        try:
            task = Task.objects.get(id=pk)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                tags=request.data.get('tags')
                for x in tags:
                    if not Tag.objects.filter(name=x).exists():
                        Tag.objects.create(name=x)
                tag_id=[]
                for x in tags:
                    tag_id.append(int(Tag.objects.get(name=x).id))
                serializer.save(tags=tag_id)
                return Response({'message':'Your data has been Updated successfully '})
        except:
            return Response({"Error message": "Check the id of the post you are trying to update "})
        return Response(serializer.errors)


# <----------------------FOR  PARTIAL DATA UPDATE --------------->
    def patch(self, request,pk, format=None):
        try:
            task = Task.objects.get(id=pk)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                tags=request.data.get('tags')
                for x in tags:
                    if not Tag.objects.filter(name=x).exists():
                        Tag.objects.create(name=x)
                tag_id=[]
                for x in tags:
                    tag_id.append(int(Tag.objects.get(name=x).id))
                serializer.save(tags=tag_id)
                return Response({'message':'Your data has been Updated successfully '})
        except:
            return Response({"Error message": "Check the id of the post you are trying to update ", 'default':'default'})
        return Response(serializer.errors)

    def delete(self, request,pk, format=None):
        try:
            task = Task.objects.get(id=pk)
            task.delete()
            return Response({'message':'Your data has been Deleted  '})
        except:
            return Response({'message': "The data you are requesting is not available or deleted "})
        




# <--------------------------------- VIEWS FOR THE TO-DO APP --------------------->

def Home(request):
 # <----------------- If user is logged in -------------------->
    tags=Tag.objects.all()
    if request.user.is_authenticated:       
        form = TaskCreate()
        task= Task.objects.filter(user=request.user).order_by('-created')
 # <...........Processing the form data....................> 
        if request.method=='POST':
            title=request.POST.get('title')
            description=request.POST.get('description')
            due_date=request.POST.get('due_date')
            status=request.POST.get('status')
            all_tags=[x.name for x in Tag.objects.all()]
            tag_id=[]
            for x in all_tags:
                if request.POST.get(x):
                    tag_id.append(int(request.POST.get(x)))
            task1=Task.objects.create(title=title,description=description,due_date=due_date,user=request.user, status=status)
            for x in tag_id:
                task1.tags.add(Tag.objects.get(id=x))
# <-------------------------------Saving the tags -------------------->
            form=TaskCreate()
            messages.success(request, 'Your task has been created successfully ')

 #<----------------- for anonymous user------------------->
    else:
        task= Task.objects.filter(user=None).order_by('-created')
        form = TaskCreate()
        if request.method=='POST':
            title=request.POST.get('title')
            description=request.POST.get('description')
            due_date=request.POST.get('due_date')
            status=request.POST.get('status')
            all_tags=[x.name for x in Tag.objects.all()]
            tag_id=[]
            for x in all_tags:
                if request.POST.get(x):
                    tag_id.append(int(request.POST.get(x)))
            task1=Task.objects.create(title=title,description=description,due_date=due_date,user=None, status=status)
            for x in tag_id:
                task1.tags.add(Tag.objects.get(id=x))
            messages.success(request, 'Your task has been created successfully ')
            return redirect('/')
    context={'form':form,'task':task, 'tags':tags }
    return render(request, 'to_do/index.html', context)

def AddTags(request):
    if request.method=='POST':
        tags = request.POST.get('tags')
        if not Tag.objects.filter(name=tags).exists():
            tag=Tag(name=tags)
            tag.save()
    return redirect('/')


# <--------------------------Edit Your Post ------------------->
def EditPost(request, pk):
    task = Task.objects.get(id=pk)
    tags=Tag.objects.all()
    form = TaskCreate(instance=task)
    if request.method=='POST':
        form = TaskCreate(request.POST, instance=task)
        if form.is_valid():
            instance=form.save(commit=False)
            if request.user.is_authenticated:
                instance.user=request.user
            else:
                instance.user = None
            instance.save()
            all_tags=[x.name for x in Tag.objects.all()]
            tag_id=[]
            for x in all_tags:
                if request.POST.get(x):
                    tag_id.append(int(request.POST.get(x)))
            for x in tags:
                instance.tags.remove(Tag.objects.get(id=x.id))
            instance.save()
            for x in tag_id:
                instance.tags.add(Tag.objects.get(id=x))
            messages.success(request, 'Your task has been Edited successfully ')
            return redirect('/')
    context={'form':form, 'task':task, 'tags':tags}

    return render(request, 'to_do/edit.html', context)

def DeleteTags(request, pk):
    if request.user.is_superuser:
        tags=Tag.objects.get(id=pk)
        tags.delete()
    else:
         messages.error(request, 'You are not allowed to delete this ask your admin to delete tags ')
    return redirect('/')


# <------------------------Delete Post ---------------------->
def DeletePost(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    messages.success(request, 'Your task has been Deleted successfully ')
    return redirect('/')


# <----------------------Creating User-------------------->
def Create_User(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in as '+ request.user.username)
        return redirect('/')
    else:
        form = UserCreate()
        if request.method=='POST':
            form = UserCreate(request.POST)
            if form.is_valid():
                user = form.save()
                UserProfile.objects.create(user=user, username=user.username, email=user.email)
                messages.success(request, 'User created Successfully '+ user.username)
                return redirect('/login/')
        context={'form':form}
        return render(request, 'to_do/sigin.html', context)


# <---------------------Loggin User--------------->

def Login_User(request): 
    if request.user.is_authenticated:
        messages.info(request, 'You are  logged in as '+ request.user.username)
        return redirect('/')
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            messages.info(request, 'You are  logged in as '+ request.user.username)
            return redirect('/')   
        else:
            messages.warning(request, ' Check your  Username or password and try again ')
    return render(request, 'to_do/login.html')

# <--------------------LogoutUser------------------->/
def LogoutUser(request):
    logout(request)
    messages.success(request, 'You are  Logged out Login or Register to use the app ')
    return redirect('/')




# def GetDropDownCountry(request):
    
# #    country= Country objects.all()
#     return render(request, 'to_do/login.html')

# def GetState(request):
#     data =json.loads(request.body)
#     city = {'city1':'delhi', 'city2':'mumbai', 'city3':'chennai'}
#     context={'city':city}

#     return JsonResponse(context)

# def GetCity(request):
#     data =json.loads(request.body)
#     city = {'city1':'rajghat', 'city2':'ashok nagar', 'city3':'vaishali'}
#     context={'city':city}

#     return JsonResponse(context)