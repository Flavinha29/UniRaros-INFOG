# accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

class StatusBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                # ✅ CORREÇÃO: Só bloqueia PACIENTES não aprovados
                # ✅ ADMINISTRADORES e STAFF podem sempre fazer login
                if user.user_type == 'patient' and user.status != 'approved':
                    raise PermissionDenied(
                        "Seu cadastro está pendente de aprovação. "
                        "Você receberá um e-mail quando for aprovado."
                    )
                return user
        except UserModel.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        # ✅ CORREÇÃO: Só pacientes precisam de aprovação
        # ✅ Administradores e staff podem sempre autenticar
        if user.user_type == 'patient':
            return user.status == 'approved'
        return True  # ✅ Admins e staff sempre podem