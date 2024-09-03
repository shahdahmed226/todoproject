from django.shortcuts import render , get_object_or_404 , redirect

#return http response 
from django.http import HttpResponse
#IMPORT MODELS
from .models import Task , Category ,Todo
from .forms import TaskForm , CategoryForm

from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm
#  Create your views here.

#   Function base view 


def index(request):
    #SELECT * from Task ;
    tasks = Task.objects.all().order_by('due_date')
    # tasks = Task.objects.filter(status ='PENDING' )
    categories = Category.objects.all()

    context = { 'tasks':tasks ,
                'categories' :categories
              }
    # return HttpResponse(tasks)
    return render(request , 'main/index.html',context)


def detailed_task(request ,id):
    
    # task = Task.objects.get(id=id)
    task = get_object_or_404(Task , id=id)

    context = {
        'task':task
    }
    return render(request , 'main/detailed.html' , context)


def todo_by_status(request , st):
    todos = Task.objects.filter(status = st)
    context = {
        'todos' :todos
    }
    return render(request , 'main/todosstatus.html' , context)


def tasks_by_status(request,status):
    tasks=Todo.objeects.filter(status=status)
    return render(request,'tasks_by_status.html',{'tasks':tasks ,'status':status})


def tasks_by_category(request,category_id):
    Category=Category.objects.get(id=category_id)
    tasks = Todo.objects.filter(Category=Category)
    return render(request,'tasks_by_category.html',{'tasks':tasks,'category':Category})




def Todo_list_Category(request  , id):
    todos = Task.objects.filter(category=id)
    categories = Category.objects.all()

    context = {
        "tasks" : todos ,
        'categories' :categories

    }
    return render(request , 'main/index.html',context)


#create task 
def Createtodo(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid() :
            form.save() #--> save the record in database            
            return redirect('home')
    else:  
        form = TaskForm()
    return render(request , 'main/create_todo.html' ,{'form' :form} )



def createCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid() :
            form.save() #--> save the record in database            
            return redirect('home')
    else:  
        form = CategoryForm()
    return render(request , 'main/createCategorys.html' ,{'form':form})



def update_task(request , id ):
    task = get_object_or_404(Task , id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST , instance=task)
        if form.is_valid() :
            form.save()            
            return redirect('home')
    else:  
        form = TaskForm(instance=task)
    return render(request, 'main/updatetask.html' , {'form':form})

def delete_task(request , id):
    task = get_object_or_404(Task , id=id)
    task.delete()
    return redirect('home')




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('home')  # Redirect to home or any other page after successful login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})



    








   # Custom login view
class CustomLoginView(LoginView):
    template_name = 'myapp/login.html'
    redirect_authenticated_user = True  # Redirect authenticated users automatically

    def get_success_url(self):
        # Redirect to a URL after successful login
        return reverse_lazy('home')  # Replace 'home' with your desired URL name

# Custom logout view
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect(reverse_lazy('home'))  # Redirect to home after registration
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

 

