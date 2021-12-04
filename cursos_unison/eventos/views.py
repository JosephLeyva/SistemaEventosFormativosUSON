from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

from .forms import *
# Create your views here.
from .models import *
from .decorators import *

# ----- USUARIOS LOGIN Y LOGOUT

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'inicio.html', context)

@unauthenticated_user
def registro(request):
    form = CrearUsuarioForm()

    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,f"Usuario {user} creado con exito")

            return redirect('login')
    
    context = {'form':form}
    return render(request,'registro.html',context)

@unauthenticated_user
def loginPag(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.info(request, 'Nombre de usuario o contraseña incorrecto')
    context = {}
    return render(request, 'login.html', context)

def logoutUsuario(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def verPerfil(request):
    context = {}
    return render(request,'ver_perfil.html',context)

@login_required(login_url='login')
def editarPerfil(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request,'editar_perfil.html',context)


# --------------------------------------------------------------------------------------#
@login_required(login_url='login')
@allowed_users(allowed_roles=['RESPONSABLE'])
def PropuestasEventosFormativos(request):
    responsable = request.user
    eventosformativos = request.user.evento_set.all()
    propuesta_count = eventosformativos.count()
    context = {'eventosformativos':eventosformativos, 'propuesta_count':propuesta_count,'responsable':responsable}
    return render(request,'PropuestasEventosFormativos.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['RESPONSABLE'])
def Propuesta(request,pk):
    evento = Evento.objects.get(id=pk)
    context = {'evento':evento}
    return render(request,'Propuesta.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['RESPONSABLE'])
def updatePropuesta(request, pk):
    evento = Evento.objects.get(id=pk)
    form = EventoForm(instance=evento)

    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('PropuestasEventosFormativos')
    context = {'form': form}
    return render(request,'Propuesta_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['RESPONSABLE'])
def createPropuesta(request,pk):
    responsable = Responsable.objects.get(id=pk)
    form = EventoForm(initial={'responsable':responsable})
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('PropuestasEventosFormativos')

    context = {'form': form,'responsable':responsable}
    return render(request,'Propuesta_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['RESPONSABLE'])
def deletePropuesta(request, pk):
    evento = Evento.objects.get(id=pk)
    if request.method == 'POST':
        evento.delete()
        return redirect('PropuestasEventosFormativos')
    return render(request,'borrar_evento.html', {'obj':evento})