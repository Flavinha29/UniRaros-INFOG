from django import forms
from .models import Relato, Comentario

class RelatoForm(forms.ModelForm):
    class Meta:
        model = Relato
        fields = ['titulo', 'texto']


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escreva seu comentário...'}),
        }
