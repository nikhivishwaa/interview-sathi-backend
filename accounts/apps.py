from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # def ready(self):
    #     from accounts.signals import handle_profile_pic, pre_save, User

    #     pre_save.connect(handle_profile_pic, sender=User)
