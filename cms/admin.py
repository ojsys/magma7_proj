from django.contrib import admin
from .models import (
    HeroSlide, SiteSettings, Program, Service, Partner, Testimonial, RichPage,
    AboutPage, CoreValue, WhyChooseUsItem, AboutGalleryImage, AboutStatistic,
    Facility, TeamMember, FacilitiesPage, TeamPage
)


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active", "created_at")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("title",)
    ordering = ("order", "id")
    fieldsets = (
        ('Slide Information', {
            'fields': ('title', 'image_url')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order'),
            'description': 'Control which slides are shown and in what order'
        }),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "email", "phone")
    fieldsets = (
        ('Basic Information', {
            'fields': ('brand_name', 'tagline', 'phone', 'email', 'address')
        }),
        ('Hero Section', {
            'fields': ('hero_headline', 'hero_subtext', 'hero_cta_text', 'hero_cta_url', 'hero_image_url')
        }),
        ('Free Guide', {
            'fields': ('free_guide_title', 'free_guide_description', 'free_guide_text', 'free_guide_url'),
            'description': 'Configure the free guide offer that appears in the hero section'
        }),
        ('Call-to-Action Section', {
            'fields': ('cta_headline', 'cta_description', 'cta_image_url', 'cta_primary_text', 'cta_primary_url', 'cta_secondary_text', 'cta_secondary_url'),
            'description': 'Configure the call-to-action section at the bottom of pages'
        }),
        ('Theme Colors', {
            'fields': ('primary_color', 'accent_color', 'light_color', 'dark_bg', 'card_bg'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "rating")
    search_fields = ("name", "quote")


@admin.register(RichPage)
class RichPageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "slug")


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ("hero_title", "updated_at")
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image_url')
        }),
        ('Our Story', {
            'fields': ('story_title', 'story_content', 'story_image_url')
        }),
        ('Mission & Vision', {
            'fields': ('mission_title', 'mission_content', 'mission_icon',
                      'vision_title', 'vision_content', 'vision_icon')
        }),
        ('Why Choose Us Section', {
            'fields': ('why_choose_title', 'why_choose_description')
        }),
        ('Gallery Section', {
            'fields': ('gallery_title', 'gallery_description')
        }),
        ('Call-to-Action', {
            'fields': ('cta_title', 'cta_description', 'cta_button_text',
                      'cta_button_url', 'cta_image_url')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one AboutPage instance
        return not AboutPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(WhyChooseUsItem)
class WhyChooseUsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(AboutGalleryImage)
class AboutGalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(AboutStatistic)
class AboutStatisticAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("label", "value")


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "order", "is_featured", "is_active")
    list_editable = ("order", "is_featured", "is_active")
    list_filter = ("is_featured", "is_active")
    search_fields = ("name", "description")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "role_category", "experience_years", "order", "is_featured", "is_active")
    list_editable = ("order", "is_featured", "is_active")
    list_filter = ("role_category", "is_featured", "is_active")
    search_fields = ("name", "role", "bio")
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'role', 'role_category', 'bio', 'image_url', 'experience_years')
        }),
        ('Professional Details', {
            'fields': ('specialties', 'certifications')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'instagram', 'linkedin')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
    )


@admin.register(FacilitiesPage)
class FacilitiesPageAdmin(admin.ModelAdmin):
    list_display = ("hero_title", "updated_at")
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image_url')
        }),
        ('Introduction', {
            'fields': ('intro_title', 'intro_content')
        }),
        ('Call-to-Action', {
            'fields': ('cta_title', 'cta_description', 'cta_button_text', 'cta_button_url')
        }),
    )

    def has_add_permission(self, request):
        return not FacilitiesPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TeamPage)
class TeamPageAdmin(admin.ModelAdmin):
    list_display = ("hero_title", "updated_at")
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image_url')
        }),
        ('Introduction', {
            'fields': ('intro_title', 'intro_content')
        }),
        ('Call-to-Action', {
            'fields': ('cta_title', 'cta_description', 'cta_button_text', 'cta_button_url')
        }),
    )

    def has_add_permission(self, request):
        return not TeamPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

