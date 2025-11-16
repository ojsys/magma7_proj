from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from .models import (
    MediaAsset, HeroSlide, SiteSettings, Program, Service, Partner, Testimonial, RichPage,
    AboutPage, CoreValue, WhyChooseUsItem, AboutGalleryImage, AboutStatistic,
    Facility, TeamMember, FacilitiesPage, TeamPage, HomeGalleryImage, ErrorLog
)


def _to_bool(value):
    """Best-effort coercion of string/int values like '1'/'0' to Python bool."""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        s = value.strip().lower()
        if s in {"1", "true", "t", "yes", "y", "on"}:
            return True
        if s in {"0", "false", "f", "no", "n", "off", ""}:
            return False
        return bool(s)
    return bool(value)


class SafeBooleanAdminMixin:
    """Mixin to safely display boolean-like fields even when DB stores '0'/'1' as TEXT.
    Replaces raw boolean fields in list_display with *_icon methods when inline editing
    isn't available (field not in list_editable) or when the user lacks change permission.
    """

    boolean_fields = ("is_active", "is_featured", "is_approved", "use_as_hero")

    def get_list_display(self, request):
        cols = list(getattr(self, "list_display", ()))
        editable = set(getattr(self, "list_editable", ()))

        def to_icon(name):
            return f"{name}_icon"

        # Replace problematic booleans with icon methods when appropriate
        replaced = []
        for i, name in enumerate(cols):
            if name in self.boolean_fields:
                needs_icon = (name not in editable) or (not self.has_change_permission(request))
                if needs_icon:
                    cols[i] = to_icon(name)
                    replaced.append(name)

        # If any replacements happened, ensure corresponding methods exist
        return tuple(cols)

    # Generic icon renderers (used if field exists on the object)
    def is_active_icon(self, obj):
        return _to_bool(getattr(obj, "is_active", False))

    is_active_icon.boolean = True
    is_active_icon.short_description = "Active"
    is_active_icon.admin_order_field = "is_active"

    def is_featured_icon(self, obj):
        return _to_bool(getattr(obj, "is_featured", False))

    is_featured_icon.boolean = True
    is_featured_icon.short_description = "Featured"
    is_featured_icon.admin_order_field = "is_featured"

    def is_approved_icon(self, obj):
        return _to_bool(getattr(obj, "is_approved", False))

    is_approved_icon.boolean = True
    is_approved_icon.short_description = "Approved"
    is_approved_icon.admin_order_field = "is_approved"

    def use_as_hero_icon(self, obj):
        return _to_bool(getattr(obj, "use_as_hero", False))

    use_as_hero_icon.boolean = True
    use_as_hero_icon.short_description = "Hero"
    use_as_hero_icon.admin_order_field = "use_as_hero"

@admin.register(MediaAsset)
class MediaAssetAdmin(SafeBooleanAdminMixin, admin.ModelAdmin):
    list_display = ("thumbnail_preview", "title", "asset_type", "usage", "file_url_list", "file_size_display", "dimensions_display", "created_at", "is_active")
    list_filter = ("asset_type", "usage", "is_active", "created_at")
    search_fields = ("title", "description", "alt_text")
    list_editable = ("is_active",)
    readonly_fields = ("preview", "file_url_display", "file_size", "width", "height", "uploaded_by", "created_at", "updated_at")
    change_list_template = 'admin/cms/mediaasset/change_list.html'

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

    def _absolute_url(self, url: str) -> str:
        if not url:
            return ''
        if url.startswith('http://') or url.startswith('https://'):
            return url
        base = getattr(settings, 'SITE_URL', '').rstrip('/')
        if not base:
            return url
        if not url.startswith('/'):
            url = '/' + url
        return f"{base}{url}"

    def file_url_display(self, obj):
        if obj.file:
            url = self._absolute_url(obj.get_absolute_url())
            return format_html('<input type="text" value="{}" readonly style="width: 100%; padding: 8px; font-family: monospace;" onclick="this.select(); document.execCommand(\'copy\'); alert(\'URL copied to clipboard!\');" />', url)
        return '—'
    file_url_display.short_description = 'File URL (click to copy)'

    def file_url_list(self, obj):
        if obj.file:
            url = self._absolute_url(obj.get_absolute_url())
            return format_html(
                '<input type="text" value="{}" readonly '
                'style="width: 260px; padding: 4px 6px; font-family: monospace; font-size: 11px;" '
                'onclick="this.select(); document.execCommand(\'copy\');" />',
                url
            )
        return '—'
    file_url_list.short_description = 'URL'

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

    actions = ['create_home_gallery_from_assets']

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def create_home_gallery_from_assets(self, request, queryset):
        from .models import HomeGalleryImage
        # Determine starting order
        try:
            next_order = (HomeGalleryImage.objects.order_by('-order').first().order or 0) + 1
        except Exception:
            next_order = 1
        created = 0
        for asset in queryset:
            if asset.asset_type != 'image':
                continue
            url = asset.get_absolute_url()
            if not url:
                continue
            # Avoid duplicates by url
            if HomeGalleryImage.objects.filter(image_url=url).exists():
                continue
            HomeGalleryImage.objects.create(title=asset.title.rsplit('.',1)[0], image_url=url, order=next_order, is_active=True)
            next_order += 1
            created += 1
        self.message_user(request, f"Created {created} home gallery image(s).")
    create_home_gallery_from_assets.short_description = "Add to Home Gallery (create items)"


@admin.register(HeroSlide)
class HeroSlideAdmin(SafeBooleanAdminMixin, admin.ModelAdmin):
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

    # SafeBooleanAdminMixin handles list display swapping/icon rendering


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
        ('Hero Stats', {
            'fields': (
                ('hero_stat1_icon', 'hero_stat1_number', 'hero_stat1_label'),
                ('hero_stat2_icon', 'hero_stat2_number', 'hero_stat2_label'),
                ('hero_stat3_icon', 'hero_stat3_number', 'hero_stat3_label'),
            ),
            'description': 'Configure the three statistics displayed in the hero section (e.g., Members, Programs, Trainers). Use Material Icons names for icons.'
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
class TestimonialAdmin(SafeBooleanAdminMixin, admin.ModelAdmin):
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
class CoreValueAdmin(SafeBooleanAdminMixin, admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(WhyChooseUsItem)
class WhyChooseUsItemAdmin(SafeBooleanAdminMixin, admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(AboutGalleryImage)
class AboutGalleryImageAdmin(SafeBooleanAdminMixin, admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(HomeGalleryImage)
class HomeGalleryImageAdmin(SafeBooleanAdminMixin, admin.ModelAdmin):
    list_display = ("thumb", "title", "order", "use_as_hero", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "use_as_hero")
    search_fields = ("title", "description")
    fields = ("title", "image_url", "description", "order", "is_active")
    change_list_template = 'admin/cms/homegalleryimage/change_list.html'

    actions = ["set_as_hero", "clear_hero"]

    def thumb(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="width:60px;height:40px;object-fit:cover;border-radius:4px"/>', obj.image_url)
        return '—'
    thumb.short_description = 'Preview'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Ensure a single hero when toggled on
        if getattr(obj, 'use_as_hero', False):
            type(obj).objects.exclude(pk=obj.pk).update(use_as_hero=False)

    def set_as_hero(self, request, queryset):
        qs = queryset.order_by('order')
        if qs.exists():
            the_one = qs.first()
            type(the_one).objects.update(use_as_hero=False)
            the_one.use_as_hero = True
            the_one.save(update_fields=["use_as_hero"])
            self.message_user(request, f"'{the_one.title}' is now the Facilities hero image.")
        else:
            self.message_user(request, "No items selected.")
    set_as_hero.short_description = "Set selected as Facilities hero (single)"

    def clear_hero(self, request, queryset):
        updated = queryset.update(use_as_hero=False)
        self.message_user(request, f"Cleared hero flag on {updated} item(s).")
    clear_hero.short_description = "Clear hero flag on selected"


@admin.register(AboutStatistic)
class AboutStatisticAdmin(SafeBooleanAdminMixin, admin.ModelAdmin):
    list_display = ("label", "value", "icon", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("label", "value")



@admin.register(Facility)
class FacilityAdmin(SafeBooleanAdminMixin, admin.ModelAdmin):
    list_display = ("name", "icon", "order", "is_featured", "is_active")
    list_editable = ("order", "is_featured", "is_active")
    list_filter = ("is_featured", "is_active")
    search_fields = ("name", "description")
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'icon', 'image_url', 'features')
        }),
        ('Display', {
            'fields': ('order', 'is_featured', 'is_active')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(SafeBooleanAdminMixin, admin.ModelAdmin):
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




@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('severity_badge', 'timestamp', 'short_message', 'path', 'user', 'resolved_badge', 'action_buttons')
    list_filter = ('severity', 'resolved', 'timestamp', 'exception_type')
    search_fields = ('message', 'path', 'user', 'exception_type', 'traceback')
    readonly_fields = ('timestamp', 'severity', 'message', 'path', 'method', 'user', 'ip_address',
                      'user_agent', 'exception_type', 'traceback_display', 'resolved_at', 'resolved_by')
    ordering = ('-timestamp',)  # Show newest errors first
    # date_hierarchy = 'timestamp'  # Disabled: requires MySQL timezone tables

    fieldsets = (
        ('Error Information', {
            'fields': ('timestamp', 'severity', 'message', 'exception_type')
        }),
        ('Request Details', {
            'fields': ('path', 'method', 'user', 'ip_address', 'user_agent')
        }),
        ('Technical Details', {
            'fields': ('traceback_display',),
            'classes': ('collapse',),
            'description': 'Full error traceback for debugging'
        }),
        ('Resolution', {
            'fields': ('resolved', 'resolved_at', 'resolved_by', 'notes')
        }),
    )

    actions = ['mark_as_resolved', 'mark_as_unresolved', 'delete_old_errors']

    def severity_badge(self, obj):
        colors = {
            'DEBUG': '#6c757d',
            'INFO': '#0dcaf0',
            'WARNING': '#ffc107',
            'ERROR': '#dc3545',
            'CRITICAL': '#8b0000',
        }
        color = colors.get(obj.severity, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 10px; border-radius: 3px; font-weight: bold; font-size: 11px;">{}</span>',
            color, obj.severity
        )
    severity_badge.short_description = 'Severity'

    def short_message(self, obj):
        msg = obj.message[:100]
        if len(obj.message) > 100:
            msg += '...'
        return msg
    short_message.short_description = 'Message'

    def resolved_badge(self, obj):
        if obj.resolved:
            return format_html('<span style="color: #28a745; font-weight: bold;">✓ Resolved</span>')
        return format_html('<span style="color: #dc3545; font-weight: bold;">✗ Unresolved</span>')
    resolved_badge.short_description = 'Status'

    def action_buttons(self, obj):
        if not obj.resolved:
            return format_html(
                '<a class="button" href="{}">Mark Resolved</a>',
                f'/admin/cms/errorlog/{obj.pk}/change/'
            )
        return '—'
    action_buttons.short_description = 'Actions'

    def traceback_display(self, obj):
        if obj.traceback:
            return format_html('<pre style="background: #f8f9fa; padding: 15px; border: 1px solid #dee2e6; border-radius: 4px; overflow-x: auto; font-size: 12px; font-family: monospace;">{}</pre>', obj.traceback)
        return 'No traceback available'
    traceback_display.short_description = 'Error Traceback'

    def mark_as_resolved(self, request, queryset):
        for error in queryset:
            error.mark_resolved(request.user)
        self.message_user(request, f'{queryset.count()} error(s) marked as resolved.')
    mark_as_resolved.short_description = 'Mark selected errors as resolved'

    def mark_as_unresolved(self, request, queryset):
        queryset.update(resolved=False, resolved_at=None, resolved_by='')
        self.message_user(request, f'{queryset.count()} error(s) marked as unresolved.')
    mark_as_unresolved.short_description = 'Mark selected errors as unresolved'

    def delete_old_errors(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        thirty_days_ago = timezone.now() - timedelta(days=30)
        old_errors = ErrorLog.objects.filter(timestamp__lt=thirty_days_ago, resolved=True)
        count = old_errors.count()
        old_errors.delete()
        self.message_user(request, f'Deleted {count} resolved error(s) older than 30 days.')
    delete_old_errors.short_description = 'Delete resolved errors older than 30 days'

    def has_add_permission(self, request):
        # Errors are added automatically, not manually
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Show superusers all errors, regular staff only their own
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user.username)
        return qs
