from django.contrib import admin
from django.utils.html import format_html
from .models import (
    MediaAsset, HeroSlide, SiteSettings, Program, Service, Partner, Testimonial, RichPage,
    AboutPage, CoreValue, WhyChooseUsItem, AboutGalleryImage, AboutStatistic,
    Facility, TeamMember, FacilitiesPage, TeamPage
)


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("thumbnail_preview", "title", "asset_type", "usage", "file_size_display", "dimensions_display", "created_at", "is_active")
    list_filter = ("asset_type", "usage", "is_active", "created_at")
    search_fields = ("title", "description", "alt_text")
    list_editable = ("is_active",)
    readonly_fields = ("preview", "file_url_display", "file_size", "width", "height", "uploaded_by", "created_at", "updated_at")

    class Media:
        css = {
            'all': ('admin/css/bulk_upload_button.css',)
        }
    fieldsets = (
        ('Upload File', {
            'fields': ('file', 'preview')
        }),
        ('Asset Information', {
            'fields': ('title', 'description', 'asset_type', 'usage', 'alt_text')
        }),
        ('File Details', {
            'fields': ('file_url_display', 'file_size', 'width', 'height'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.asset_type == 'image' and obj.file:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.file.url)
        return '—'
    thumbnail_preview.short_description = 'Preview'

    def preview(self, obj):
        if obj.file:
            if obj.asset_type == 'image':
                return format_html('<img src="{}" style="max-width: 500px; max-height: 300px; border: 1px solid #ddd; padding: 5px;" />', obj.file.url)
            elif obj.asset_type == 'video':
                return format_html('<video src="{}" controls style="max-width: 500px;"></video>', obj.file.url)
        return 'No file uploaded yet'
    preview.short_description = 'File Preview'

    def file_url_display(self, obj):
        if obj.file:
            url = obj.get_absolute_url()
            return format_html('<input type="text" value="{}" readonly style="width: 100%; padding: 8px; font-family: monospace;" onclick="this.select(); document.execCommand(\'copy\'); alert(\'URL copied to clipboard!\');" />', url)
        return '—'
    file_url_display.short_description = 'File URL (click to copy)'

    def file_size_display(self, obj):
        if obj.file_size:
            # Convert bytes to human-readable format
            size = obj.file_size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return '—'
    file_size_display.short_description = 'Size'

    def dimensions_display(self, obj):
        if obj.width and obj.height:
            return f"{obj.width} × {obj.height}px"
        return '—'
    dimensions_display.short_description = 'Dimensions'

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview", "order", "is_active", "created_at")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("title",)
    ordering = ("order", "id")
    readonly_fields = ("image_preview_large",)
    fieldsets = (
        ('Slide Image', {
            'fields': ('image', 'image_preview_large', 'image_url'),
            'description': 'Upload an image OR provide an external URL'
        }),
        ('Slide Information', {
            'fields': ('title',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order'),
            'description': 'Control which slides are shown and in what order'
        }),
    )

    def image_preview(self, obj):
        url = obj.get_image_url()
        if url:
            return format_html('<img src="{}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 4px;" />', url)
        return '—'
    image_preview.short_description = 'Preview'

    def image_preview_large(self, obj):
        url = obj.get_image_url()
        if url:
            return format_html('<img src="{}" style="max-width: 600px; max-height: 300px; border: 1px solid #ddd; padding: 5px;" />', url)
        return 'No image uploaded or URL provided yet'
    image_preview_large.short_description = 'Image Preview'


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("brand_name", "email", "phone")
    readonly_fields = ("logo_preview", "favicon_preview")
    fieldsets = (
        ('Branding', {
            'fields': ('brand_name', 'tagline', 'logo', 'logo_preview', 'logo_url', 'favicon', 'favicon_preview', 'favicon_url'),
            'description': 'Upload logo/favicon OR provide URLs. Uploaded files take priority.'
        }),
        ('Basic Information', {
            'fields': ('phone', 'email', 'address')
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

    def logo_preview(self, obj):
        url = obj.get_logo_url()
        if url:
            return format_html('<img src="{}" style="max-height: 60px; max-width: 300px; border: 1px solid #ddd; padding: 5px;" />', url)
        return 'No logo uploaded or URL provided'
    logo_preview.short_description = 'Logo Preview'

    def favicon_preview(self, obj):
        url = obj.get_favicon_url()
        if url:
            return format_html('<img src="{}" style="width: 32px; height: 32px; border: 1px solid #ddd; padding: 2px;" />', url)
        return 'No favicon uploaded or URL provided'
    favicon_preview.short_description = 'Favicon Preview'

    def has_add_permission(self, request):
        # Only allow one SiteSettings instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


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

