from django.shortcuts import render
from reserva_material.models import Pessoa, Quartel, Material, Cautela
from reserva_material.forms import emprestarForm, receberForm, CadastrarPessoa
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import datetime
from reserva_material.views import pdfgen

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
            # return HttpResponseRedirect(reverse('imprimir_cautela', kwargs={'identidade': '1111111111'}))
            # return HttpResponse(request, 'imprimir_cautela')

            return pdfgen.imprimir_cautela(request)
            # return HttpResponse('<center><h1><u>SUCESSO</u>!</h1></center>', status=200)
    else:
        formulario = emprestarForm()
    return render(request, 'acoes/emprestar.html', {'formulario': formulario})

@login_required
def receber(request):
    if request.method == 'POST':
        formulario = receberForm(request.POST)
        if formulario.is_valid():
            identidade_recebe = request.POST.get('identidade_recebe')
            senha_recebe = request.POST.get('senha_recebe')
            lista_materiais = request.POST.getlist('material_recebido')
            quantitativo = 1
            try:
                pessoa_recebe = Pessoa.objects.get(identidade_militar=identidade_recebe, senha=senha_recebe)
            except:
                return HttpResponse('<center><h1>Usuário ou senha <u>INCORRETA</u>!</h1></center>', status=400)
            for item in lista_materiais:
                item = Material.objects.get(id=item)
                cautela = Cautela.objects.filter(material_cautelado=item).order_by('-inicio_cautela')[0]
                if cautela.pessoa_emprestou == pessoa_recebe:
                    item.em_cautela = False
                    item.em_reserva = True
                    cautela.vencida = False
                    cautela.devolvido = True
                    cautela.data_devolucao = timezone.now()
                    cautela.save()
                    item.save()
    else:
        formulario = receberForm()
    return render(request, 'acoes/receber.html', {'formulario': formulario})

@login_required
def cadastrar_pessoa(request):
    if request.method == 'POST':
        formulario = CadastrarPessoa(request.POST)
        # return HttpResponse('Antes de validar!')
        if not formulario.is_valid():
            # return HttpResponse('Após validar!')
            pessoa = Pessoa(
                nome_completo = request.POST.get('nome_completo'),
                nome_guerra = request.POST.get('nome_guerra'),
                posto_graduacao = request.POST.get('posto_graduacao'),
                identidade_civil = request.POST.get('identidade_civil'),
                identidade_militar = request.POST.get('identidade_militar'),
                cpf = request.POST.get('cpf'),
                senha = request.POST.get('senha'),
                quartel_atual = Quartel.objects.get(id=request.POST.get('quartel_atual')),
                telefone_pessoal = request.POST.get('telefone_pessoal'),
                telefone_quartel = request.POST.get('telefone_quartel'),
                email = request.POST.get('email')
                )
            pessoa.save()
            return HttpResponse('Pessoa registrada com sucesso!')
    else:
        formulario = CadastrarPessoa()
    return render(request, 'acoes/cadastrar_pessoa.html', {'formulario': formulario})
