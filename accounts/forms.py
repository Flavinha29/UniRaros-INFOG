# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Paciente

class UserCreationFormCustom(UserCreationForm):
    tipo_usuario = forms.ChoiceField(choices=User.TIPO_CHOICES, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "tipo_usuario")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = self.cleaned_data["tipo_usuario"]
        if commit:
            user.save()
            # se for paciente, já cria o perfil relacionado
            if user.tipo_usuario == "paciente":
                Paciente.objects.create(user=user, nome_completo=user.username, email=user.email)
        return user
