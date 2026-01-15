from django.utils.text import slugify


def generate_unique_slug(model_class, title, allow_unicode=True):
    """Generate unique slug for a model instance"""
    base_slug = slugify(title, allow_unicode=allow_unicode)
    slug = base_slug
    counter = 1

    while model_class.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug

