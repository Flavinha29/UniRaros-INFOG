import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordValidator:
    def validate(self, password, user=None):
        errors = []
        
        if len(password) < 8:
            errors.append('A senha deve ter no mínimo 8 caracteres.')
        
        if not re.search(r'[A-Z]', password):
            errors.append('A senha deve conter pelo menos 1 letra maiúscula.')
        
        if not re.search(r'[a-z]', password):
            errors.append('A senha deve conter pelo menos 1 letra minúscula.')
        
        if not re.search(r'[0-9]', password):
            errors.append('A senha deve conter pelo menos 1 número.')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('A senha deve conter pelo menos 1 caractere especial (!@#$%&* etc.).')
        
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _(
            "Sua senha deve conter:\n"
            "- Mínimo 8 caracteres\n"
            "- Pelo menos 1 letra maiúscula\n" 
            "- Pelo menos 1 letra minúscula\n"
            "- Pelo menos 1 número\n"
            "- Pelo menos 1 caractere especial (!@#$%&* etc.)"
        )