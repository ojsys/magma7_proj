from django.shortcuts import render
from cms.models import (
    HeroSlide, SiteSettings, Program, Service, Partner, Testimonial,
    AboutPage, CoreValue, WhyChooseUsItem, AboutGalleryImage, AboutStatistic,
    Facility, TeamMember, FacilitiesPage, TeamPage, HomeGalleryImage
)
from memberships.models import Plan
from django.db.models import Avg


def home(request):
    settings_obj = SiteSettings.objects.first()
    programs = Program.objects.all()[:8]
    services = Service.objects.all()[:8]
    partners = Partner.objects.all()[:8]
    testimonials = Testimonial.objects.filter(is_approved=True)[:6]
    avg_rating = testimonials.aggregate(avg=Avg('rating'))['avg'] or 0
    plans = Plan.objects.filter(is_active=True).order_by('price')[:3]  # Get up to 3 active plans
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')
    gallery_images = HomeGalleryImage.objects.filter(is_active=True).order_by('order')[:8]  # Get up to 8 gallery images
    ctx = {
        'site_settings': settings_obj,
        'programs': programs,
        'services': services,
        'partners': partners,
        'testimonials': testimonials,
        'avg_rating': round(avg_rating, 1),
        'plans': plans,
        'hero_slides': hero_slides,
        'gallery_images': gallery_images,
    }
    return render(request, 'core/home.html', ctx)


def about(request):
    about_page = AboutPage.objects.first()
    core_values = CoreValue.objects.filter(is_active=True)
    why_choose_items = WhyChooseUsItem.objects.filter(is_active=True)
    gallery_images = AboutGalleryImage.objects.filter(is_active=True)
    statistics = AboutStatistic.objects.filter(is_active=True)

    ctx = {
        'about_page': about_page,
        'core_values': core_values,
        'why_choose_items': why_choose_items,
        'gallery_images': gallery_images,
        'statistics': statistics,
    }
    return render(request, 'core/about.html', ctx)


def facilities(request):
    facilities_page = FacilitiesPage.objects.first()
    facilities = Facility.objects.filter(is_active=True)
    featured_facilities = facilities.filter(is_featured=True)[:3]
    # Load all active home gallery images for full collage on facilities page
    gallery_images = HomeGalleryImage.objects.filter(is_active=True).order_by('order')
    # Determine hero background: prefer explicit FacilitiesPage hero, else first gallery image
    hero_bg_url = ''
    # 1) Prefer an explicitly chosen HomeGalleryImage hero
    hero_img = HomeGalleryImage.objects.filter(is_active=True, use_as_hero=True).order_by('order').first()
    if hero_img:
        hero_bg_url = hero_img.image_url
    # 2) Else use FacilitiesPage hero if defined
    elif facilities_page and getattr(facilities_page, 'hero_image_url', ''):
        hero_bg_url = facilities_page.hero_image_url
    # 3) Else fallback to first gallery image
    else:
        first_img = gallery_images.first()
        if first_img:
            hero_bg_url = first_img.image_url

    ctx = {
        'facilities_page': facilities_page,
        'facilities': facilities,
        'featured_facilities': featured_facilities,
        'gallery_images': gallery_images,
        'hero_bg_url': hero_bg_url,
    }
    return render(request, 'core/facilities.html', ctx)


def team(request):
    team_page = TeamPage.objects.first()
    team_members = TeamMember.objects.filter(is_active=True)
    featured_members = team_members.filter(is_featured=True)[:4]

    ctx = {
        'team_page': team_page,
        'team_members': team_members,
        'featured_members': featured_members,
    }
    return render(request, 'core/team.html', ctx)


def mission(request):
    return render(request, 'core/mission.html')


def vision(request):
    return render(request, 'core/vision.html')


def values(request):
    return render(request, 'core/values.html')


def careers(request):
    return render(request, 'core/careers.html')
