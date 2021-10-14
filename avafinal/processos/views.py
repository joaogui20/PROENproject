from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib import messages
from .models import Process
from .forms import ProcessForm

# Create your views here.
def helloWorld(request):
    return HttpResponse('Hello World')

@login_required
def newProcess(request):
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            process = form.save(commit=False)
            process.done = 'Registrado'
            process.user = request.user
            process.save()
            return redirect('/')
    else:
        form = ProcessForm()
        return render(request, 'processos/addprocess.html', {'form': form})

@login_required
def processList(request):
    search = request.GET.get('search')
    if search:
        process = Process.objects.filter(title_icontains=search, user=request.user)
    else:
        process_list = Process.objects.all().order_by('-created_at').filter(user=request.user)
        paginator = Paginator(process_list, 5)
        page = request.GET.get('page')
        process = paginator.get_page(page)
    return render(request, 'processos/list.html', {'process': process})

@login_required
def processView(request, id):
    process = get_object_or_404(Process, pk=id)
    return render(request, 'processos/process.html', {'process': process})

@login_required
def editProcess(request, id):
    process = get_object_or_404(Process, pk=id)
    form = ProcessForm(instance=process)

    if(request.method == 'POST'):
        form = ProcessForm(request.POST, instance=process)
        if(form.is_valid()):
            process.save()
            return redirect('/')
        else:
            return render(request, 'processos/editprocess.html', {'form': form, 'process': process})
    else:
        return render(request, 'processos/editprocess.html', {'form': form, 'process': process})

@login_required
def deleteProcess(request, id):
    process = get_object_or_404(Process, pk=id)
    process.delete()
    messages.info(request, 'Processo deletado com sucesso!')
    return redirect('/')

def yourName(request, name):
    return render(request, 'processos/yourname.html', {'name': name})
