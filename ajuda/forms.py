from django import forms
from .models import PedidoAjuda

class PedidoAjudaForm(forms.ModelForm):
    class Meta:
        model = PedidoAjuda
        fields = ['titulo', 'descricao']  # ✅ USA OS CAMPOS DO MODELO
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Resumo do seu problema ou dúvida'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva detalhadamente o que você precisa...',
                'rows': 5
            }),
        }
        labels = {
            'titulo': 'Assunto',
            'descricao': 'Descrição detalhada'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ REMOVE OS CAMPOS nome e email, pois o usuário já está logado
        # O sistema automaticamente associa o usuário logado