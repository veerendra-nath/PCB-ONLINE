from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.utils.functional import LazyObject


class GerberArchives(S3Boto3Storage):
    location = 'gerber_archives/'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


gerber_storage = GerberArchives()
