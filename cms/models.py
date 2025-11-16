from django.db import models
from django.core.validators import FileExtensionValidator


class MediaAsset(models.Model):
    """Media Center - Centralized media asset management"""
    ASSET_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('other', 'Other'),
    )

    USAGE_CHOICES = (
        ('logo', 'Logo'),
        ('favicon', 'Favicon'),
        ('hero', 'Hero Image'),
        ('slide', 'Slide Background'),
        ('gallery', 'Gallery Image'),
        ('profile', 'Profile Photo'),
        ('thumbnail', 'Thumbnail'),
        ('icon', 'Icon'),
        ('general', 'General Use'),
    )

    title = models.CharField(max_length=200, help_text='Descriptive title for this asset')
    description = models.TextField(blank=True, help_text='Optional description or notes')
    file = models.FileField(
        upload_to='media_assets/%Y/%m/',
        help_text='Upload file (images, videos, documents)',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp', 'mp4', 'webm', 'pdf', 'ico'])]
    )
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES, default='image')
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, default='general', help_text='Primary usage of this asset')
    alt_text = models.CharField(max_length=200, blank=True, help_text='Alt text for images (SEO)')

    # Metadata
    file_size = models.PositiveIntegerField(null=True, blank=True, help_text='File size in bytes')
    width = models.PositiveIntegerField(null=True, blank=True, help_text='Image width in pixels')
    height = models.PositiveIntegerField(null=True, blank=True, help_text='Image height in pixels')

    uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Media Asset'
        verbose_name_plural = 'Media Center'

    def __str__(self):
        return f"{self.title} ({self.get_asset_type_display()})"

    def get_absolute_url(self):
        """Returns the full URL to access this file"""
        if self.file:
            return self.file.url
        return ''

    def save(self, *args, **kwargs):
        # Auto-set file size and dimensions if it's an image
        if self.file:
            self.file_size = self.file.size

            # Try to get image dimensions
            try:
                from PIL import Image
                img = Image.open(self.file)
                self.width, self.height = img.size
            except:
                pass

        super().save(*args, **kwargs)


class HeroSlide(models.Model):
    """Hero background slides for home page"""
    title = models.CharField(max_length=200, help_text='Slide title for admin reference')
    image = models.ImageField(upload_to='hero_slides/', blank=True, null=True, help_text='Upload image (recommended: 1920x1080px or larger)')
    image_url = models.URLField(blank=True, help_text='OR provide image URL (if not uploading)')
    is_active = models.BooleanField(default=True, help_text='Show this slide in rotation')
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower numbers show first)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'

    def __str__(self):
        return f"{self.title} (Order: {self.order})"

    def get_image_url(self):
        """Returns uploaded image URL if available, otherwise returns provided URL"""
        if self.image:
            return self.image.url
        return self.image_url or ''


class SiteSettings(models.Model):
    brand_name = models.CharField(max_length=100, default='Magma7Fitness')
    tagline = models.CharField(max_length=200, blank=True)

    # Logo and Favicon - Upload OR URL
    logo = models.ImageField(upload_to='branding/', blank=True, null=True, help_text='Upload logo (PNG/SVG with transparent background)')
    logo_url = models.URLField(blank=True, help_text='OR provide logo URL')
    favicon = models.FileField(upload_to='branding/', blank=True, null=True, help_text='Upload favicon (.ico or .png, 32x32 or 64x64 pixels)', validators=[FileExtensionValidator(allowed_extensions=['ico', 'png'])])
    favicon_url = models.URLField(blank=True, help_text='OR provide favicon URL')

    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    hero_headline = models.CharField(max_length=200, blank=True)
    hero_subtext = models.TextField(blank=True)
    hero_cta_text = models.CharField(max_length=50, blank=True)
    hero_cta_url = models.CharField(max_length=200, blank=True)
    hero_image_url = models.URLField(blank=True)

    # Free Guide Settings
    free_guide_text = models.CharField(max_length=50, default='Get Now', help_text='Text shown on the free guide button')
    free_guide_url = models.URLField(blank=True, help_text='URL to download or access the free guide (PDF, form, etc.)')
    free_guide_title = models.CharField(max_length=100, default='Free Fitness Guide', blank=True, help_text='Title of the free guide for admin reference')
    free_guide_description = models.TextField(blank=True, help_text='Description of what the free guide contains')

    # CTA Section Settings
    cta_headline = models.CharField(max_length=200, default='Ready to Start?', help_text='Main headline for CTA section')
    cta_description = models.TextField(default='Join thousands of satisfied members who have transformed their lives at Magma7Fitness', help_text='Description text for CTA section')
    cta_image_url = models.URLField(blank=True, help_text='Background or feature image for CTA section')
    cta_primary_text = models.CharField(max_length=50, default='Sign Up Today', help_text='Text for primary CTA button')
    cta_primary_url = models.CharField(max_length=200, default='/accounts/signup/', help_text='URL for primary CTA button')
    cta_secondary_text = models.CharField(max_length=50, default='Learn More', help_text='Text for secondary CTA button')
    cta_secondary_url = models.CharField(max_length=200, default='/about/', help_text='URL for secondary CTA button')

    primary_color = models.CharField(max_length=7, default='#0b6e4f')  # green
    accent_color = models.CharField(max_length=7, default='#d4af37')   # gold
    light_color = models.CharField(max_length=7, default='#ffffff')    # white
    dark_bg = models.CharField(max_length=7, default='#121416')
    card_bg = models.CharField(max_length=7, default='#1d1f21')

    # Hero Stats
    hero_stat1_icon = models.CharField(max_length=50, default='groups', help_text='Material icon name for first stat')
    hero_stat1_number = models.CharField(max_length=20, default='970+', help_text='Number to display (e.g., 970+, 1K+)')
    hero_stat1_label = models.CharField(max_length=50, default='Members', help_text='Label for first stat')

    hero_stat2_icon = models.CharField(max_length=50, default='sports_gymnastics', help_text='Material icon name for second stat')
    hero_stat2_number = models.CharField(max_length=20, default='135+', help_text='Number to display (e.g., 135+, 200+)')
    hero_stat2_label = models.CharField(max_length=50, default='Programs', help_text='Label for second stat')

    hero_stat3_icon = models.CharField(max_length=50, default='workspace_premium', help_text='Material icon name for third stat')
    hero_stat3_number = models.CharField(max_length=20, default='105+', help_text='Number to display (e.g., 105+, 50+)')
    hero_stat3_label = models.CharField(max_length=50, default='Trainers', help_text='Label for third stat')

    def __str__(self):
        return 'Site Settings'

    def get_logo_url(self):
        """Returns uploaded logo URL if available, otherwise returns provided URL"""
        if self.logo:
            return self.logo.url
        return self.logo_url or ''

    def get_favicon_url(self):
        """Returns uploaded favicon URL if available, otherwise returns provided URL"""
        if self.favicon:
            return self.favicon.url
        return self.favicon_url or ''


class Program(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Material icon name')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Partner(models.Model):
    name = models.CharField(max_length=120)
    logo_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    quote = models.TextField()
    avatar_url = models.URLField(blank=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.rating}★)"


class RichPage(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title


class AboutPage(models.Model):
    """Main about page content - only one instance should exist"""

    # Hero Section
    hero_title = models.CharField(max_length=200, default='About Magma7Fitness')
    hero_subtitle = models.TextField(blank=True, help_text='Brief introduction text')
    hero_image_url = models.URLField(blank=True, help_text='Main hero image')

    # Our Story Section
    story_title = models.CharField(max_length=200, default='Our Story')
    story_content = models.TextField(help_text='Tell your gym\'s story')
    story_image_url = models.URLField(blank=True, help_text='Image for story section')

    # Mission Section
    mission_title = models.CharField(max_length=200, default='Our Mission')
    mission_content = models.TextField()
    mission_icon = models.CharField(max_length=50, default='track_changes', help_text='Material icon name')

    # Vision Section
    vision_title = models.CharField(max_length=200, default='Our Vision')
    vision_content = models.TextField()
    vision_icon = models.CharField(max_length=50, default='visibility', help_text='Material icon name')

    # Why Choose Us Section
    why_choose_title = models.CharField(max_length=200, default='Why Choose Us')
    why_choose_description = models.TextField(blank=True)

    # Gallery Section
    gallery_title = models.CharField(max_length=200, default='Our Facility')
    gallery_description = models.TextField(blank=True)

    # CTA Section
    cta_title = models.CharField(max_length=200, default='Ready to Transform?')
    cta_description = models.TextField(default='Join our community today')
    cta_button_text = models.CharField(max_length=50, default='Get Started')
    cta_button_url = models.CharField(max_length=200, default='/memberships/plans/')
    cta_image_url = models.URLField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Page Content'
        verbose_name_plural = 'About Page Content'

    def __str__(self):
        return 'About Page Content'


class CoreValue(models.Model):
    """Core values displayed on about page"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='star', help_text='Material icon name')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Core Value'
        verbose_name_plural = 'Core Values'

    def __str__(self):
        return self.title


class WhyChooseUsItem(models.Model):
    """Reasons why customers should choose us"""
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='check_circle', help_text='Material icon name')
    image_url = models.URLField(blank=True, help_text='Optional image')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Why Choose Us Item'
        verbose_name_plural = 'Why Choose Us Items'

    def __str__(self):
        return self.title


class AboutGalleryImage(models.Model):
    """Gallery images for about page"""
    title = models.CharField(max_length=150, help_text='Image title/caption')
    image_url = models.URLField(help_text='Image URL')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'About Gallery Image'
        verbose_name_plural = 'About Gallery Images'

    def __str__(self):
        return self.title


class AboutStatistic(models.Model):
    """Key statistics to display on about page"""
    label = models.CharField(max_length=100, help_text='e.g., "Active Members"')
    value = models.CharField(max_length=50, help_text='e.g., "5000+"')
    icon = models.CharField(max_length=50, default='trending_up', help_text='Material icon name')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'About Statistic'
        verbose_name_plural = 'About Statistics'

    def __str__(self):
        return f"{self.label}: {self.value}"


class Facility(models.Model):
    """Gym facilities"""
    name = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fitness_center', help_text='Material icon name')
    image_url = models.URLField(blank=True, help_text='Facility image')
    features = models.TextField(blank=True, help_text='Comma-separated features list')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Show in featured section')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return self.name

    def get_features_list(self):
        """Return features as a list"""
        if self.features:
            return [f.strip() for f in self.features.split(',')]
        return []


class TeamMember(models.Model):
    """Team members/staff"""
    ROLE_CHOICES = (
        ('trainer', 'Fitness Trainer'),
        ('nutritionist', 'Nutritionist'),
        ('manager', 'Manager'),
        ('instructor', 'Instructor'),
        ('support', 'Support Staff'),
        ('specialist', 'Specialist'),
    )

    name = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    role_category = models.CharField(max_length=20, choices=ROLE_CHOICES, default='trainer')
    bio = models.TextField(help_text='Brief biography')
    image_url = models.URLField(help_text='Profile photo')
    specialties = models.TextField(blank=True, help_text='Comma-separated specialties')
    certifications = models.TextField(blank=True, help_text='Certifications and qualifications')
    experience_years = models.PositiveIntegerField(default=0, help_text='Years of experience')

    # Social links
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Show in featured section')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return f"{self.name} - {self.role}"

    def get_specialties_list(self):
        """Return specialties as a list"""
        if self.specialties:
            return [s.strip() for s in self.specialties.split(',')]
        return []


class FacilitiesPage(models.Model):
    """Facilities page content"""
    hero_title = models.CharField(max_length=200, default='Our World-Class Facilities')
    hero_subtitle = models.TextField(blank=True)
    hero_image_url = models.URLField(blank=True)

    intro_title = models.CharField(max_length=200, default='Everything You Need')
    intro_content = models.TextField(blank=True)

    cta_title = models.CharField(max_length=200, default='Ready to Experience It?')
    cta_description = models.TextField(default='Visit us for a free tour')
    cta_button_text = models.CharField(max_length=50, default='Book a Tour')
    cta_button_url = models.CharField(max_length=200, default='/contact/')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Facilities Page Content'
        verbose_name_plural = 'Facilities Page Content'

    def __str__(self):
        return 'Facilities Page Content'


class TeamPage(models.Model):
    """Team page content"""
    hero_title = models.CharField(max_length=200, default='Meet Our Team')
    hero_subtitle = models.TextField(blank=True)
    hero_image_url = models.URLField(blank=True)

    intro_title = models.CharField(max_length=200, default='Expert Guidance')
    intro_content = models.TextField(blank=True)

    cta_title = models.CharField(max_length=200, default='Join Our Team')
    cta_description = models.TextField(default='We\'re always looking for talented individuals')
    cta_button_text = models.CharField(max_length=50, default='View Careers')
    cta_button_url = models.CharField(max_length=200, default='/careers/')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Team Page Content'
        verbose_name_plural = 'Team Page Content'

    def __str__(self):
        return 'Team Page Content'


class HomeGalleryImage(models.Model):
    """Gallery images for homepage facility showcase"""
    title = models.CharField(max_length=150, help_text='Image title/caption')
    image_url = models.URLField(help_text='Image URL (from Media Center or external)')
    description = models.TextField(blank=True, help_text='Optional description shown on hover')
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower numbers first)')
    is_active = models.BooleanField(default=True, help_text='Show this image in the gallery')
    use_as_hero = models.BooleanField(default=False, help_text='Use this image as the Facilities page hero background')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Home Gallery Image'
        verbose_name_plural = 'Home Gallery Images'

    def __str__(self):
        return self.title


class ErrorLog(models.Model):
    """Store application errors for admin viewing"""
    SEVERITY_CHOICES = (
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    )

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='ERROR', db_index=True)
    message = models.TextField(help_text='Error message')
    path = models.CharField(max_length=500, blank=True, help_text='URL path where error occurred')
    method = models.CharField(max_length=10, blank=True, help_text='HTTP method (GET, POST, etc.)')
    user = models.CharField(max_length=150, blank=True, help_text='Username if authenticated')
    ip_address = models.GenericIPAddressField(blank=True, null=True, help_text='Client IP address')
    user_agent = models.TextField(blank=True, help_text='Browser user agent')
    exception_type = models.CharField(max_length=200, blank=True, help_text='Exception class name')
    traceback = models.TextField(blank=True, help_text='Full error traceback')
    resolved = models.BooleanField(default=False, help_text='Mark as resolved')
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolved_by = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True, help_text='Admin notes about this error')

    class Meta:
        verbose_name = 'Error Log'
        verbose_name_plural = 'Error Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['severity']),
            models.Index(fields=['resolved']),
        ]

    def __str__(self):
        return f"[{self.severity}] {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.message[:50]}"

    def mark_resolved(self, user):
        """Mark error as resolved"""
        from django.utils import timezone
        self.resolved = True
        self.resolved_at = timezone.now()
        self.resolved_by = user.username if hasattr(user, 'username') else str(user)
        self.save()
