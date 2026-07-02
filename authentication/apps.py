from django.apps import AppConfig


# class AuthenticationConfig(AppConfig):
#     name = 'authentication'


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication' # timro app ko name

    def ready(self):
        import authentication.signals # signals lai connect gareko