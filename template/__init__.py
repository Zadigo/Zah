def get_template_backend():
    from zah.settings import settings
    return getattr(settings, 'TEMPLATE_BACKEND', None)
