from django import forms
from reserva_material.models import Material, Quartel

class emprestarForm(forms.Form):
    identidade_empresta = forms.CharField(required=True, min_length=10, max_length=10, widget=forms.TextInput())
    senha_empresta = forms.CharField(widget=forms.PasswordInput())
    identidade_retira = forms.CharField(required=True, min_length=10, max_length=10, widget=forms.TextInput())
    senha_retira = forms.CharField(widget=forms.PasswordInput())
    material_cautelado = forms.ModelMultipleChoiceField(queryset=Material.objects.filter(em_reserva=True), widget=forms.SelectMultiple())

class receberForm(forms.Form):
    identidade_recebe = forms.CharField(required=True, min_length=10, max_length=10, widget=forms.TextInput())
    senha_recebe = forms.CharField(widget=forms.PasswordInput())
    material_recebido = forms.ModelMultipleChoiceField(queryset=Material.objects.filter(em_cautela=True), widget=forms.SelectMultiple())

class CadastrarPessoa(forms.Form):
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
    ('Asp', 'Asp'),
    ('ST', 'ST'),
    ('1º Sgt', '1º Sgt'),
    ('2º Sgt', '2º Sgt'),
    ('3º Sgt', '3º Sgt'),
    ('Cb', 'Cb'),
    ('Sd', 'Sd'),
    ('Sd EV', 'Sd EV'),
    )
    nome_completo = forms.CharField(required=True)
    nome_guerra = forms.CharField(required=True)
    posto_graduacao = forms.ChoiceField(required=True, choices=posto_graduacao_choices)
    identidade_civil = forms.CharField(required=True, min_length=9, max_length=9)
    identidade_militar = forms.CharField(required=True, min_length=10, max_length=10)
    cpf = forms.CharField(required=True, min_length=11, max_length=11)
    senha = forms.CharField(required=True, widget=forms.PasswordInput())
    quartel_atual = forms.ModelChoiceField(queryset=Quartel.objects.all(), empty_label=None, widget=forms.SelectMultiple())
    telefone_pessoal = forms.CharField(min_length=10, max_length=11)
    telefone_quartel = forms.CharField(min_length=10, max_length=10)
    email = forms.EmailField()
    foto = forms.ImageField(required=False)
