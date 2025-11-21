from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import os


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'


# initialize firebase app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(BASE_DIR, "service-account.json"))

firebase_app = None
if not firebase_admin._apps:
    firebase_app = firebase_admin.initialize_app(cred)
