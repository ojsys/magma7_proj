# Generated migration for adding MediaAsset model and file upload fields

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '0002_add_logo_favicon_to_sitesettings'),
    ]

    operations = [
        # Create MediaAsset model
        migrations.CreateModel(
            name='MediaAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(upload_to='media_assets/%Y/%m/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp', 'mp4', 'webm', 'pdf', 'ico'])])),
                ('asset_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('document', 'Document'), ('other', 'Other')], default='image', max_length=20)),
                ('usage', models.CharField(choices=[('hero', 'Hero Slide'), ('logo', 'Logo/Branding'), ('service', 'Service Image'), ('team', 'Team Photo'), ('facility', 'Facility Photo'), ('gallery', 'Gallery'), ('general', 'General Use')], default='general', max_length=20)),
                ('alt_text', models.CharField(blank=True, help_text='Alt text for accessibility', max_length=200)),
                ('file_size', models.PositiveIntegerField(blank=True, null=True)),
                ('width', models.PositiveIntegerField(blank=True, null=True)),
                ('height', models.PositiveIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Media Asset',
                'verbose_name_plural': 'Media Assets',
                'ordering': ['-created_at'],
            },
        ),

        # Add image field to HeroSlide
        migrations.AddField(
            model_name='heroslide',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='hero_slides/'),
        ),

        # Add logo field to SiteSettings
        migrations.AddField(
            model_name='sitesettings',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='branding/'),
        ),

        # Add favicon field to SiteSettings
        migrations.AddField(
            model_name='sitesettings',
            name='favicon',
            field=models.FileField(blank=True, null=True, upload_to='branding/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico', 'png'])]),
        ),
    ]
