from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from reserva_material.models import Material, Cautela, Pessoa
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime, timedelta

width, height = A4
estilo_tabela = TableStyle([
    ('FONTNAME', (0,0), (-1,1), 'Times-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Times-Roman'),
    ('BOX', (0,0), (-1,-1), 2, colors.black),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,0), 2, colors.black),
    ('INNERGRID', (0,0), (-1,0), 2, colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
])

def gerar_pdf(request, titulo):
    datahora = datetime.now()
    response = HttpResponse(content_type='application/pdf')
    filename = '%s_%s' % (titulo, datahora.strftime("%d-%m-%Y %H:%M:%S"))
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % (filename)
    c = canvas.Canvas(response, pagesize=A4)
    c.setFont('Times-Roman', 12)
    return response, c, datahora

def gerar_cabecalho(canvas):
    canvas.setFont('Times-Bold', 12)
    canvas.drawImage('reserva_material/static/config/selo.png', width/2-50, height-100, 100, 100)
    posicao_y = height-120
    try:
        subordinacao = open('reserva_material/static/config/cabecalho.txt', 'r')
    except:
        return canvas, posicao_y
    for linha in subordinacao:
        canvas.drawCentredString(width/2, posicao_y, linha[:-1])
        posicao_y -= 10
    posicao_y -= 10
    return canvas, posicao_y

def gerar_texto_cautela(canvas, posicao_y):
    canvas.setFont('Times-Roman', 12)
    texto = open('reserva_material/static/config/texto_cautela.txt', 'r')
    for linha in texto:
        canvas.drawString(30, posicao_y, linha[:-1])
        posicao_y -= 10
    posicao_y -= 10
    return canvas, posicao_y

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
    table.setStyle(estilo_tabela)
    table.wrapOn(canvas, width, height)
    table.drawOn(canvas, 20, posicao_y-20*len(data))
    return canvas

def gerar_rodape(canvas, texto):
    canvas.drawRightString(width-10, 10, texto)
    return canvas

def gerar_tabela_cautela(canvas, posicao_y, request):
    header = ['Quantidade', 'Nome do Material', 'Número de Série', 'Alterações']
    data = []
    data.append(header)
    pessoa = Pessoa.objects.get(identidade_militar=request.POST.get('identidade_retira'))
    lista_materiais = request.POST.getlist('material_cautelado')
    for item in lista_materiais:
        item = Material.objects.get(id=item)
        quantidade = 1
        nome = item.nome_material
        numero_serie = item.numero_serie
        alteracoes = item.descricao
        if not alteracoes:
            alteracoes = '-'
        data.append([quantidade, nome, numero_serie, alteracoes])
    table = Table(data)
    table.setStyle(estilo_tabela)
    table.wrapOn(canvas, width, height)
    table.drawOn(canvas, 20, posicao_y-20*len(data))
    return canvas

def gerar_assinatura(canvas, request):
    posicao_y = 50
    pessoa = Pessoa.objects.get(identidade_militar=request.POST.get('identidade_retira'))
    canvas.setFont('Times-Bold', 12)
    texto = (
        '_________________________________________________',
        '%s - %s' % (pessoa.nome_completo, pessoa.posto_graduacao),
        '',
    )
    for linha in texto:
        canvas.drawCentredString(width/2, posicao_y, linha)
        posicao_y -= 20
    posicao_y -= 20
    canvas.setFont('Times-Roman', 12)
    return canvas

def gerar_rodape(canvas, datahora):
    canvas.drawString(10, 10, 'INÍCIO: ' + datahora.strftime("%d-%m-%Y %H:%M:%S"))
    datahora = datahora + timedelta(days=30)
    canvas.drawRightString(width-10, 10, 'VENCIMENTO: ' + datahora.strftime("%d-%m-%Y %H:%M:%S"))
    return canvas

def estruturar_pdf(canvas, tipo, datahora, request):
    canvas, posicao_y = gerar_cabecalho(canvas)
    if tipo == 'CAUTELA':
        canvas, posicao_y = gerar_texto_cautela(canvas, posicao_y)
        canvas = gerar_tabela_cautela(canvas, posicao_y, request)
        canvas = gerar_rodape(canvas, datahora)
        canvas = gerar_assinatura(canvas, request)
    else:
        canvas.drawCentredString(width/2, posicao_y, 'Pronto da reserva de material do Pelotão Posto de Comando')
        canvas = gerar_tabela(canvas, posicao_y)
        canvas.drawRightString(width-10, 10, 'DATA: ' + datahora.strftime("%d-%m-%Y %H:%M:%S"))
    return canvas

@login_required
def imprimir_pronto(request):
    tipo = 'PRONTO'
    response, c, datahora = gerar_pdf(request, tipo)
    c = estruturar_pdf(c, tipo, datahora, request)
    c.showPage()
    c.save()
    return response

@login_required
def imprimir_cautela(request):
    tipo = 'CAUTELA'
    response, c, datahora = gerar_pdf(request, tipo)
    c = estruturar_pdf(c, tipo, datahora, request)
    c.showPage()
    c.save()
    return response
