from django.db import models


class HeroSlide(models.Model):
    """Hero background slides for home page"""
    title = models.CharField(max_length=200, help_text='Slide title for admin reference')
    image_url = models.URLField(help_text='Background image URL (use high-quality images, min 1920x1080)')
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


class SiteSettings(models.Model):
    brand_name = models.CharField(max_length=100, default='Magma7Fitness')
    tagline = models.CharField(max_length=200, blank=True)
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

    def __str__(self):
        return 'Site Settings'


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

