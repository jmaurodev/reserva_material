from django import forms
from reserva_material.models import Material

class emprestarForm(forms.Form):
    identidade_empresta = forms.IntegerField(min_value=0, max_value=9999999999, widget=forms.NumberInput())
    senha_empresta = forms.CharField(widget=forms.PasswordInput())
    identidade_retira = forms.IntegerField(min_value=0, max_value=9999999999, widget=forms.NumberInput())
    senha_retira = forms.CharField(widget=forms.PasswordInput())
    material_cautelado = forms.ModelMultipleChoiceField(queryset=Material.objects.filter(em_reserva=True), widget=forms.SelectMultiple())

class receberForm(forms.Form):
    identidade_recebe = forms.IntegerField(min_value=0, max_value=9999999999, widget=forms.NumberInput())
    senha_recebe = forms.CharField(widget=forms.PasswordInput())
    material_recebido = forms.ModelMultipleChoiceField(queryset=Material.objects.filter(em_cautela=True), widget=forms.SelectMultiple())
