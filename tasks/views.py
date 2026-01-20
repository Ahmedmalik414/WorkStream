from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q 
from .models import Task
from .forms import TaskForm
@login_required(login_url='login')
def task_list(request):
    # 1. Capture the search input (from <input name="search-area">)
    search_input = request.GET.get('search-area') or ''
    
    # 2. Start with all tasks belonging to the user
    tasks = Task.objects.filter(user=request.user)
    
    # 3. If there is a search term, filter the results further
    if search_input:
        # Search in title OR description (icontains = case-insensitive)
        tasks = tasks.filter(
            Q(title__icontains=search_input) | 
            Q(description__icontains=search_input)
        )
    
    tasks = tasks.order_by('-created_at')
    # Handle Task Creation form
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('task_list')
    else:
        form = TaskForm()
        
    context = {
        'tasks': tasks, 
        'form': form, 
        'search_input': search_input,
        'now': timezone.now()
    }
    return render(request, 'tasks/index.html', context)


def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user) # Only delete your own tasks!
    task.delete()
    return redirect('task_list')

def toggle_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user) # Only toggle your own tasks!
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def delete_selected_tasks(request):
    if request.method == 'POST':
        task_ids = request.POST.getlist('task_ids')
        # Security: Only delete tasks belonging to the logged-in user
        Task.objects.filter(id__in=task_ids, user=request.user).delete()
    return redirect('task_list')


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def signup_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/signup.html', {'form': form})    