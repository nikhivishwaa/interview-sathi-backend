from storages.backends.s3 import S3Storage
from django.conf import settings

class StaticStorage(S3Storage):
    location = "static"
    default_acl = None
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    file_overwrite = True


class PublicMediaStorage(S3Storage):
    location = "media/public"
    default_acl = None
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    file_overwrite = False


class PrivateMediaStorage(S3Storage):
    location = "media/private"
    default_acl = None
    custom_domain = None
    file_overwrite = False
