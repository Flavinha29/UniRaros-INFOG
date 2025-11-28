# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .validators import PasswordValidator

User = get_user_model()  # ✅ USA get_user_model() EM VEZ DE IMPORTAR DIRETO

class UserCreationFormCustom(UserCreationForm):
    # ✅ CORRIGIDO: usar user_type em vez de tipo_usuario
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,  # ✅ CORRIGIDO: USER_TYPE_CHOICES
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Tipo de Usuário"
    )
    
    phone = forms.CharField(
        max_length=20, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999'
        }),
        label="Telefone"
    )
    
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label="Data de Nascimento"
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password1',
            'placeholder': 'Digite sua senha'
        }),
        validators=[PasswordValidator()]
    )
    
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password2', 
            'placeholder': 'Digite a senha novamente'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "user_type", "phone", "birth_date")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Seu melhor e-mail'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data["user_type"]
        
        user.phone = self.cleaned_data.get("phone", "")
        user.birth_date = self.cleaned_data.get("birth_date")
        
        # ✅ CORRIGIDO: patient em vez de paciente
        if user.user_type == "patient":
            user.status = "pending"
        
        if commit:
            user.save()
            # ✅ REMOVIDO: criação de Paciente (não temos esse model)
        return user

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail cadastrado'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'new_password1',
            'placeholder': 'Nova senha'
        }),
        validators=[PasswordValidator()]
    )
    new_password2 = forms.CharField(
        label="Confirme a nova senha", 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'new_password2',
            'placeholder': 'Confirme a nova senha'
        })
    )