from django.conf import settings
from django.core.files.images import get_image_dimensions


def validate_cover(value):
    """
    validating the file size (the allowed size should be set in settings)
    """
    size = get_image_dimensions(value)
    if sum(size) > settings.MAX_UPLOAD_ADMIN_SIZE:
        raise ValueError("Please keep file size under 2 MB")
