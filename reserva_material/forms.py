from django import forms
from reserva_material.models import Material

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
