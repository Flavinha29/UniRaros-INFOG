# relatos/forms.py
from django import forms
from .models import Relato, Comentario  # ✅ ADICIONE Comentario aqui

class RelatoForm(forms.ModelForm):
    class Meta:
        model = Relato
        fields = ['titulo', 'texto']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Estilização dos campos
        self.fields['titulo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite um título para seu relato',
            'style': 'border-radius: 6px;'
        })
        
        self.fields['texto'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Compartilhe sua história...',
            'rows': 8,
            'style': 'border-radius: 6px; resize: vertical;'
        })
    
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 5:
            raise forms.ValidationError("O título deve ter pelo menos 5 caracteres.")
        if len(titulo) > 200:
            raise forms.ValidationError("O título deve ter no máximo 200 caracteres.")
        return titulo
    
    def clean_texto(self):
        texto = self.cleaned_data.get('texto')
        if len(texto) < 50:
            raise forms.ValidationError("O relato deve ter pelo menos 50 caracteres.")
        if len(texto) > 5000:
            raise forms.ValidationError("O relato deve ter no máximo 5000 caracteres.")
        return texto


# ✅ ADICIONE ESTA CLASSE PARA RESOLVER O ERRO
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']  # ✅ CORRETO: baseado no seu modelo, o campo é 'texto'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Estilização do campo de comentário
        self.fields['texto'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite seu comentário...',
            'rows': 4,
            'style': 'border-radius: 6px; resize: vertical;'
        })
    
    def clean_texto(self):
        texto = self.cleaned_data.get('texto')
        if len(texto) < 5:
            raise forms.ValidationError("O comentário deve ter pelo menos 5 caracteres.")
        if len(texto) > 1000:
            raise forms.ValidationError("O comentário deve ter no máximo 1000 caracteres.")
        return texto