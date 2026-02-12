from django.shortcuts import render, redirect
from .models import Task

def home(request):
    filter_type=request.GET.get('filter','all')
    if filter_type=='completed':
        tasks=Task.objects.filter(completed=True).order_by('-id')  
    elif filter_type=='pending':
        tasks=Task.objects.filter(completed=False).order_by('-id')  
    else:    
        tasks = Task.objects.all().order_by('-id')

    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    pending_tasks = Task.objects.filter(completed=False).count()

    return render(request, 'home.html', {
        'tasks': tasks,
        'filter_type': filter_type,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    })



def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        Task.objects.create(title=title)
        return redirect('home')
    return redirect('home')

def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('home')

def complete_task(request, id):
    task = Task.objects.get(id=id)
    task.completed = True
    task.save()
    return redirect('home')

def edit_task(request,id):
    task=Task.objects.get(id=id)
    if request.method=='POST':
        task.title=request.POST.get('title')
        task.save()
        return redirect('home')
    return render (request,'edit_task.html',{'task':task})