from django.conf import settings
from django.core.files.storage import get_storage_class

temp_storage = get_storage_class(import_path=settings.TEMP_FILE_STORAGE)
