from .models import SiteSettings

def site_settings(request):
    """
    Context processor to make site settings available in all templates.
    """
    try:
        settings = SiteSettings.objects.get(pk=1)
    except SiteSettings.DoesNotExist:
        # Return default SiteSettings instance if none exists
        settings = SiteSettings()

    return {
        'site_settings': settings
    }