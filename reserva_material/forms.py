from django import forms
from reserva_material.models import Material

class emprestarForm(forms.Form):
    attrs_idt_empresta = {
        'class': 'form-control',
        'aria-describedby': 'identidadeEmprestaHelp',
        'placeholder': 'Identidade Militar de quem empresta',
    }
    attrs_idt_retira = {
            'class': 'form-control',
            'aria-describedby': 'identidadeRetiraHelp',
            'placeholder': 'Identidade Militar de quem retira',
    }
    attrs_senha_retira = {
            'class': 'form-control',
            'placeholder': 'Senha de quem retira',
    }
    attrs_senha_empresta = {
            'class': 'form-control',
            'placeholder': 'Senha de quem empresta',
    }
    attrs_mat_cautelado = {
        'class': 'form-control',
        'aria-describedby': 'identidadeEmprestaHelp',
        'placeholder': 'Identidade Militar de quem empresta',
    }

    material = Material.objects.all()
    lista_materiais = []
    for item in material:
        lista_materiais.append((item.id, ('%s - %s' % (item.nome_material, item.numero_serie))))

    identidade_empresta = forms.IntegerField(min_value=0, max_value=9999999999, widget=forms.NumberInput(attrs=attrs_idt_empresta))
    senha_empresta = forms.CharField(widget=forms.PasswordInput(attrs=attrs_senha_empresta))
    identidade_retira = forms.IntegerField(min_value=0, max_value=9999999999, widget=forms.NumberInput(attrs=attrs_idt_retira))
    senha_retira = forms.CharField(widget=forms.PasswordInput(attrs=attrs_senha_retira))
    material_cautelado = forms.ChoiceField(choices=lista_materiais, widget=forms.Select(attrs=attrs_mat_cautelado))
