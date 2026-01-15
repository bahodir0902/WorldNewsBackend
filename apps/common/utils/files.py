import os
import uuid


def unique_image_path(instance, filename):
    """Generate unique path for uploaded images"""
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"

    # Use model name as folder
    model_name = instance.__class__.__name__.lower()
    return os.path.join(model_name, unique_filename)

