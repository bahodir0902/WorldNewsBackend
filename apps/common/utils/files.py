import os
import uuid


def unique_image_path(instance, filename):
    """Generate unique path for uploaded images"""
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"

    # Use model name as folder
    model_name = instance.__class__.__name__.lower()
    return os.path.join(model_name, unique_filename)


def unique_video_path(instance, filename):
    """Generate unique path for uploaded videos"""
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"

    # Use model name as folder with 'videos' subfolder
    model_name = instance.__class__.__name__.lower()
    return os.path.join(f"{model_name}_videos", unique_filename)

