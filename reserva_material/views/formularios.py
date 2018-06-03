from django.shortcuts import render
from reserva_material.models import Pessoa, Quartel, Material, Cautela
from reserva_material.forms import emprestarForm
from django.contrib.auth.decorators import login_required

@login_required
def emprestar(request):
    status = ''
    if request.method == 'POST':
        formulario = emprestarForm(request.POST)
        if formulario.is_valid():
            identidade_empresta = request.POST.get('identidade_empresta')
            senha_empresta = request.POST.get('senha_empresta')
            identidade_retira = request.POST.get('identidade_retira')
            senha_retira = request.POST.get('senha_retira')
            material_cautelado = Material.objects.get(id=request.POST.get('material_cautelado'))
            quantitativo = 1
            try:
                pessoa_empresta = Pessoa.objects.get(identidade_militar=identidade_empresta, senha=senha_empresta)
            except:
                status = 'Identidade ou senha da pessoa que empresta o material estão erradas!'
            try:
                pessoa_retira = Pessoa.objects.get(identidade_militar=identidade_retira, senha=senha_retira)
            except:
                status = 'Identidade ou senha da pessoa que retira o material estão erradas!'
            status = '%s - %s cautelado para %s %s com sucesso!' % (material_cautelado.nome_material, material_cautelado.numero_serie, pessoa_retira.posto_graduacao, pessoa_retira.nome_guerra)
    formulario = emprestarForm()
    context = {
        'formulario': formulario,
        'status': status,
    }
    return render(request, 'acoes/emprestar.html', context)

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
