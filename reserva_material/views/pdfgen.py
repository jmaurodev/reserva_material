from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from time import gmtime, strftime
from reserva_material.models import Material
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
width, height = A4

def gerar_pdf(request, titulo):
    response = HttpResponse(content_type='application/pdf')
    datahora = strftime("%d-%m-%Y %H:%M:%S", gmtime())
    filename = '%s_%s' % (titulo, datahora)
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (filename)
    return response

def gerar_cabecalho(canvas):
    canvas.setFont('Times-Bold', 12)
    canvas.drawImage('media/images/selo.png', width/2-50, height-100, 100, 100)
    posicao_y = height-120
    subordinacao = (
        'MINISTÉRIO DA DEFESA',
        'EXÉRCITO BRASILEIRO',
        '20ª COMPANHIA DE COMUNICAÇÕES PÁRA-QUEDISTA',
        '(Pelotão de Transmissões 1945)',
    )
    for linha in subordinacao:
        canvas.drawCentredString(width/2, posicao_y, linha)
        posicao_y -= 10
    posicao_y -= 10
    return canvas, posicao_y

def gerar_texto_cautela(canvas, posicao_y):
    canvas.setFont('Times-Roman', 12)
    texto = (
        'Recebi do Pelotão Posto de Comando, da 20ª Companhia de Comunicações Pára-quedista, para uso e',
        'posterior devolução, o material abaixo relacionado, sendo responsável por qualquer tipo de dano, extravio',
        'ou mau uso do equipamento.',
    )
    for linha in texto:
        if linha == texto[0]:
            canvas.drawString(40, posicao_y, linha)
            posicao_y -= 10
            continue
        canvas.drawString(30, posicao_y, linha)
        posicao_y -= 10
    posicao_y -= 10
    return canvas

def gerar_tabela(canvas, posicao_y):
    header = ['Nome do Material', 'Total', 'Rsv?', 'Cautelado?', 'Mnt?', 'Indisp?']
    data = []
    data.append(header)
    material = Material.objects.values('nome_material').annotate(total=Count('nome_material'))
    for item in material:
        nome = item.get('nome_material')
        qtd_total = item.get('total')
        qtd_em_reserva = len(Material.objects.filter(nome_material=nome, em_reserva=True))
        qtd_em_cautela = len(Material.objects.filter(nome_material=nome, em_cautela=True))
        qtd_em_manutencao = len(Material.objects.filter(nome_material=nome, em_manutencao=True))
        qtd_indisponivel = len(Material.objects.filter(nome_material=nome, indisponivel=True))
        data.append([nome, qtd_total, qtd_em_reserva, qtd_em_cautela, qtd_em_manutencao, qtd_indisponivel])
    table = Table(data)
    table.setStyle(TableStyle([
    ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
    ('BOX', (0,0), (-1,-1), 2, colors.black),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,0), 2, colors.black),
    ('INNERGRID', (0,0), (-1,0), 2, colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    table.wrapOn(canvas, width, height)
    table.drawOn(canvas, 20, posicao_y-20*len(data))
    return canvas

def gerar_rodape(canvas, texto):
    canvas.drawRightString(width-10, 10, texto)
    return canvas

@login_required
def imprimir_pronto(request):
    response = gerar_pdf(request, 'PRONTO')
    c = canvas.Canvas(response, pagesize=A4)
    c, posicao_y = gerar_cabecalho(c)
    c.setFont('Times-Roman', 12)
    c.drawCentredString(width/2, posicao_y, 'Pronto da reserva de material do Pelotão Posto de Comando')
    c = gerar_tabela(c, posicao_y)
    rodape = '1/1'
    c = gerar_rodape(c, rodape)
    c.showPage()
    c.save()
    return response

@login_required
def imprimir_cautela(request):
    response = gerar_pdf(request, 'CAUTELA')
    c = canvas.Canvas(response, pagesize=A4)
    c, posicao_y = gerar_cabecalho(c)
    c = gerar_texto_cautela(c, posicao_y)
    c.showPage()
    c.save()
    return response
