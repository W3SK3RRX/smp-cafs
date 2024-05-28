from django import forms
from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome_funcionario', 'setor', 'telefone_funcionario']
        widgets = {
            'nome_funcionario': forms.TextInput(attrs={'class': 'form-control'}),
            'setor': forms.Select(attrs={'class': 'form-control'}),
            'telefone_funcionario': forms.TextInput(attrs={'class': 'form-control'}),
        }
