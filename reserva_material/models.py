from django.db import models

class Pessoa(models.Model):
    posto_graduacao_choices = (
    ('Gen Ex', 'Gen Ex'),
    ('Gen Div', 'Gen Div'),
    ('Gen Bda', 'Gen Bda'),
    ('Cel', 'Cel'),
    ('TC', 'TC'),
    ('Maj', 'Maj'),
    ('Cap', 'Cap'),
    ('1º Ten', '1º Ten'),
    ('2º Ten', '2º Ten'),
    ('ST', 'ST'),
    ('1º Sgt', '1º Sgt'),
    ('2º Sgt', '2º Sgt'),
    ('3º Sgt', '3º Sgt'),
    ('Cb', 'Cb'),
    ('Sd', 'Sd'),
    ('Sd EV', 'Sd EV'),
    )
    nome_completo = models.CharField(max_length=100)
    nome_guerra = models.CharField(max_length=100)
    posto_graduacao = models.CharField(max_length=20, choices=posto_graduacao_choices, default='3º Sgt')
    identidade_civil = models.CharField(max_length=9)
    identidade_militar = models.CharField(max_length=10, help_text='Campo utilizado para identificar a pessoa no sistema')
    cpf = models.CharField(max_length=11)
    # Armazenar hash da senha e nao a senha propriamente dita
    senha = models.CharField(max_length=64, help_text='Funcionará como a assinatura da pessoa')
    quartel_atual = models.ForeignKey('Quartel', on_delete=models.PROTECT)
    telefone_pessoal = models.CharField(max_length=11, help_text='Principal meio utilizado para estabelecer contato com a pessoa')
    telefone_quartel = models.CharField(max_length=10)
    email = models.EmailField(help_text='Usado para enviar avisos antes do vencimento da cautela')
    foto = models.ImageField(upload_to='images/pessoa/', null=True, help_text='Imagem da pessoa')
    def __str__(self):
        texto = '%s %s - %s (%s)' % (self.posto_graduacao, self.nome_guerra, self.quartel_atual, self.telefone_pessoal)
        return texto

class Quartel(models.Model):
    nome_quartel = models.CharField(max_length=100, help_text='Usado para gerar documentos')
    sigla = models.CharField(max_length=100, help_text='Usado para facilitar a busca')
    def __str__(self):
        return self.nome_quartel

class Material(models.Model):
    nome_material = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)
    em_reserva = models.BooleanField(default=True, help_text='O material encontra-se na reserva?')
    em_cautela = models.BooleanField(default=False, help_text='O material encontra-se cautelado?')
    em_manutencao = models.BooleanField(default=False, help_text='O material encontra-se em manutenção?')
    indisponivel = models.BooleanField(default=False, help_text='O material encontra-se indisponível?')
    numero_serie = models.CharField(max_length=20, null=True, blank=True)
    foto = models.ImageField(upload_to='images/material/', null=True, blank=True, help_text='Imagem do material')
    def __str__(self):
        return self.nome_material

class Cautela(models.Model):
    pessoa_retirou = models.ForeignKey('Pessoa', on_delete=models.PROTECT, related_name='+', null=False, blank=False)
    pessoa_emprestou = models.ForeignKey('Pessoa', on_delete=models.PROTECT, related_name='+', null=False, blank=False)
    material_cautelado = models.ForeignKey('Material', on_delete=models.PROTECT, null=False, blank=False)
    quantitativo = models.IntegerField(default=1, null=False, blank=False, help_text='Quantidade de material cautelado')
    inicio_cautela = models.DateTimeField(auto_now_add=True, editable=True, help_text='')
    fim_cautela = models.DateTimeField(editable=True, help_text='Padrão de 30 dias')
    vencida = models.BooleanField(default=False, help_text='Sinaliza se a cautela está vencida')
