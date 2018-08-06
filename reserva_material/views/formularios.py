from django.shortcuts import render
from reserva_material.models import Pessoa, Quartel, Material, Cautela
from reserva_material.forms import emprestarForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import datetime

@login_required
def emprestar(request):
    if request.method == 'POST':
        formulario = emprestarForm(request.POST)
        if formulario.is_valid():
            identidade_empresta = request.POST.get('identidade_empresta')
            senha_empresta = request.POST.get('senha_empresta')
            identidade_retira = request.POST.get('identidade_retira')
            senha_retira = request.POST.get('senha_retira')
            lista_materiais = request.POST.getlist('material_cautelado')
            quantitativo = 1
            try:
                pessoa_empresta = Pessoa.objects.get(identidade_militar=identidade_empresta, senha=senha_empresta)
                pessoa_retira = Pessoa.objects.get(identidade_militar=identidade_retira, senha=senha_retira)
            except:
                return HttpResponse('<center><h1>Usuários ou senhas <u>INCORRETAS</u>!</h1></center>', status=400)
                # return HttpResponseRedirect(reverse('emprestar'))
            for item in lista_materiais:
                item = Material.objects.get(id=item)
                item.em_reserva = False
                item.em_cautela = True
                cautela = Cautela(
                pessoa_emprestou = pessoa_empresta,
                pessoa_retirou = pessoa_retira,
                material_cautelado = item,
                quantitativo = quantitativo,
                fim_cautela = timezone.now() + datetime.timedelta(days=30)
                )
                cautela.save()
                item.save()
    else:
        formulario = emprestarForm()
    return render(request, 'acoes/emprestar.html', {'formulario': formulario})

@login_required
def receber(request):
    pessoal = Pessoa.objects.all()
    material = Material.objects.all()
    cautelas = Cautela.objects.all()
    context = {
        'pessoal': pessoal,
        'material': material,
        'cautelas': cautelas,
    }
    return render(request, 'acoes/receber.html', context)
