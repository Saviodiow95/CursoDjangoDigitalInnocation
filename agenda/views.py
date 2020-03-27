from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse


def login_user(request):

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username = username, password = password)
        
        if usuario is not None: 
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou Senha invalidos")
    
    return redirect('/')


@login_required(login_url = '/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    eventos = Evento.objects.filter(usuario =usuario,
                                    data_evento__gt=data_atual)
    return render(request,'agenda.html',{'eventos':eventos})

@login_required(login_url = '/login/')
def evento(request):
    id = request.GET.get('id')
    if id:
        evento = Evento.objects.get(id=id)
        return render(request,'evento.html',{'evento': evento})
    
    return render(request,'evento.html')


@login_required(login_url = '/login/')
def submit_evento(request):
    if(request.POST):
        id = request.POST.get('id')
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user

        if id:
            Evento.objects.filter(id=id).update(titulo=titulo,
                                                data_evento=data_evento,
                                                descricao=descricao,
                                                usuario=usuario)
        else:
            Evento.objects.create(titulo=titulo,
                                data_evento=data_evento,
                                descricao=descricao,
                                usuario=usuario)
    
    return redirect('/')

@login_required(login_url = '/login/')
def delete_evento(request, id):
    usuario = request.user
    try:
        evento = Evento.objects.filter(id=id, usuario = usuario )
    except Exception:
        raise Http404

    if evento:
        evento.delete()
    else:
        raise Http404

    return redirect('/')

@login_required(login_url = '/login/')
def json_lista(request):
    usuario = request.user
    
    eventos = Evento.objects.filter(usuario =usuario).values('id','titulo')

    return JsonResponse(list(eventos),safe=False)