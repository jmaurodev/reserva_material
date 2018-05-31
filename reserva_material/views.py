from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from time import gmtime, strftime
from reserva_material.models import Pessoa, Quartel, Material, Cautela
from .forms import emprestarForm

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

def imprimir_pronto(request):
    response = HttpResponse(content_type='application/pdf')
    datahora = strftime("%d-%m-%Y %H:%M:%S", gmtime())
    filename = 'PRONTO_%s' % (datahora)
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (filename)
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    header = ['Nome do Material', 'Total', 'Rsv', 'Cautelado', 'Indisp', 'Mnt']
    data = []
    data.append(header)
    material = Material.objects.all()
    for item in material:
        data.append([item.nome_material, item.qtd_total, item.qtd_em_reserva, item.qtd_cautelado, item.qtd_indisponivel, item.qtd_em_manutencao])
    t = Table(data)
    t.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
    ('BOX', (0,0), (-1,-1), 2, colors.black),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,0), 2, colors.black),
    ('INNERGRID', (0,0), (-1,0), 2, colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    t.wrapOn(p, width, height)
    t.drawOn(p, 5*mm, 5*mm)

    p.showPage()
    p.save()
    return response
