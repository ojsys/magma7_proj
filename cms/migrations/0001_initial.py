from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('logo_url', models.URLField(blank=True)),
                ('website_url', models.URLField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(blank=True, help_text='Material icon name', max_length=50)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='RichPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(default='Magma7Fitness', max_length=100)),
                ('tagline', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('hero_headline', models.CharField(blank=True, max_length=200)),
                ('hero_subtext', models.TextField(blank=True)),
                ('hero_cta_text', models.CharField(blank=True, max_length=50)),
                ('hero_cta_url', models.CharField(blank=True, max_length=200)),
                ('hero_image_url', models.URLField(blank=True)),
                ('primary_color', models.CharField(default='#0b6e4f', max_length=7)),
                ('accent_color', models.CharField(default='#d4af37', max_length=7)),
                ('light_color', models.CharField(default='#ffffff', max_length=7)),
                ('dark_bg', models.CharField(default='#121416', max_length=7)),
                ('card_bg', models.CharField(default='#1d1f21', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('role', models.CharField(blank=True, max_length=120)),
                ('rating', models.PositiveSmallIntegerField(default=5)),
                ('quote', models.TextField()),
                ('avatar_url', models.URLField(blank=True)),
                ('is_approved', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]

