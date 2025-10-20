# Generated migration for adding logo and favicon to SiteSettings

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='logo_url',
            field=models.URLField(blank=True, help_text='URL to your site logo (PNG/SVG recommended, transparent background)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='favicon_url',
            field=models.URLField(blank=True, help_text='URL to your favicon (32x32 or 64x64 pixels, .ico or .png format)'),
        ),
    ]
