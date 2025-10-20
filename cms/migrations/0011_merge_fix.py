# Merge migration to fix conflicting branches

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_heroslide'),
        ('cms', '0010_alter_mediaasset_options_and_more'),
    ]

    operations = [
        # No operations needed - this just merges the two branches
    ]
