from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .validators import PasswordValidator

User = get_user_model()

class UserCreationFormCustom(UserCreationForm):
    # ✅ PRIMEIRO NOME OBRIGATÓRIO
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu primeiro nome'
        }),
        label="Primeiro Nome"
    )
    
    # ✅ SOBRENOME OBRIGATÓRIO
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu sobrenome'
        }),
        label="Sobrenome"
    )
    
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Tipo de Usuário"
    )
    
    # ✅ TELEFONE OBRIGATÓRIO
    phone = forms.CharField(
        max_length=20, 
        required=True,
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
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "user_type", "phone", "birth_date")
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
        user.phone = self.cleaned_data["phone"]
        
        if user.user_type == "patient":
            user.status = "pending"
        
        if commit:
            user.save()
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