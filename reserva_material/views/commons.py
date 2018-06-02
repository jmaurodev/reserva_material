from django.shortcuts import render
from reserva_material.models import Pessoa, Quartel, Material, Cautela

def index(request):
    return render(request, 'index.html')

def pessoal(request):
    pessoal = Pessoa.objects.all()
    context = {
        'pessoal': pessoal,
    }
    return render(request, 'relatorios/pessoal.html', context)

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

def cautelas_vencidas(request):
    cautelas = Cautela.objects.all()
    context = {
        'cautelas': cautelas,
    }
    return render(request, 'relatorios/cautelas_vencidas.html', context)

def pronto(request):
    materiais = Material.objects.all()
    context = {
        'materiais': materiais,
    }
    return render(request, 'relatorios/pronto.html', context)
