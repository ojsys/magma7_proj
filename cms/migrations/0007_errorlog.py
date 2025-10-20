# Generated migration for ErrorLog model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_heroslide'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('severity', models.CharField(choices=[('DEBUG', 'Debug'), ('INFO', 'Info'), ('WARNING', 'Warning'), ('ERROR', 'Error'), ('CRITICAL', 'Critical')], db_index=True, default='ERROR', max_length=20)),
                ('message', models.TextField(help_text='Error message')),
                ('path', models.CharField(blank=True, help_text='URL path where error occurred', max_length=500)),
                ('method', models.CharField(blank=True, help_text='HTTP method (GET, POST, etc.)', max_length=10)),
                ('user', models.CharField(blank=True, help_text='Username if authenticated', max_length=150)),
                ('ip_address', models.GenericIPAddressField(blank=True, help_text='Client IP address', null=True)),
                ('user_agent', models.TextField(blank=True, help_text='Browser user agent')),
                ('exception_type', models.CharField(blank=True, help_text='Exception class name', max_length=200)),
                ('traceback', models.TextField(blank=True, help_text='Full error traceback')),
                ('resolved', models.BooleanField(default=False, help_text='Mark as resolved')),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('resolved_by', models.CharField(blank=True, max_length=150)),
                ('notes', models.TextField(blank=True, help_text='Admin notes about this error')),
            ],
            options={
                'verbose_name': 'Error Log',
                'verbose_name_plural': 'Error Logs',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='errorlog',
            index=models.Index(fields=['-timestamp'], name='cms_errorlo_timesta_idx'),
        ),
        migrations.AddIndex(
            model_name='errorlog',
            index=models.Index(fields=['severity'], name='cms_errorlo_severit_idx'),
        ),
        migrations.AddIndex(
            model_name='errorlog',
            index=models.Index(fields=['resolved'], name='cms_errorlo_resolve_idx'),
        ),
    ]
