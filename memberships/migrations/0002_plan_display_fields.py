from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plan',
            name='price_period',
            field=models.CharField(default='Per Month', max_length=50),
        ),
    ]

