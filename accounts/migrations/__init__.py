# accounts/__init__.py
default_app_config = 'accounts.apps.AccountsConfig'

# Garanta que os signals sejam carregados
import accounts.signals