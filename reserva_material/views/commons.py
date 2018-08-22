from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from reserva_material.models import Pessoa, Quartel, Material, Cautela

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def pessoal(request):
    pessoal = Pessoa.objects.all()
    context = {
        'pessoal': pessoal,
    }
    return render(request, 'relatorios/pessoal.html', context)

@login_required
def material(request):
    material = Material.objects.all()
    context = {
        'material': material,
    }
    return render(request, 'relatorios/material.html', context)

def cautelas(request):
    cautelas = Cautela.objects.all()
    context = {
        'cautelas': cautelas,
    }
    return render(request, 'relatorios/cautelas.html', context)

@login_required
def cautelas_vencidas(request):
    cautelas = Cautela.objects.all()
    context = {
        'cautelas': cautelas,
    }
    return render(request, 'relatorios/cautelas_vencidas.html', context)

def deslogado(request):
    return render(request, 'acesso/deslogado.html')
