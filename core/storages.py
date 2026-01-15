from decouple import config
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    """S3 storage for public media files"""
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = False

    def __init__(self, *args, **kwargs):
        # Only use S3 if enabled in settings
        if not config('USE_S3_STORAGE', default=False, cast=bool):
            raise ValueError("S3 storage not enabled")
        super().__init__(*args, **kwargs)

