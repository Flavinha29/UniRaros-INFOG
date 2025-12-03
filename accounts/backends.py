# accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q

class StatusBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        # ✅ CORREÇÃO: Busca por username OU email, mas pega o primeiro
        try:
            # Tenta username primeiro
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            try:
                # Se não encontrar por username, tenta por email
                # ✅ CORREÇÃO: Usa filter().first() em vez de get() para evitar MultipleObjectsReturned
                user = UserModel.objects.filter(email=username).first()
                if not user:
                    return None
            except UserModel.DoesNotExist:
                return None
        except UserModel.MultipleObjectsReturned:
            # Se houver múltiplos usuários com mesmo username (improvável, mas seguro)
            user = UserModel.objects.filter(username=username).first()
        
        # Verifica a senha
        if user and user.check_password(password):
            # ✅ CORREÇÃO: Superuser sempre pode logar
            if user.is_superuser or user.is_staff:
                return user
                
            # ✅ VERIFICAÇÃO DE APROVAÇÃO PARA PACIENTES
            if user.user_type == 'patient' and user.status != 'approved':
                raise PermissionDenied(
                    "Seu cadastro está pendente de aprovação. "
                    "Você receberá um e-mail quando for aprovado."
                )
            return user
        return None

    def user_can_authenticate(self, user):
        # ✅ CORREÇÃO: Superuser e staff sempre podem
        if user.is_superuser or user.is_staff:
            return True
            
        # ✅ CORREÇÃO: Só pacientes precisam de aprovação
        if user.user_type == 'patient':
            return user.status == 'approved'
            
        return True  # ✅ Outros tipos sempre podem