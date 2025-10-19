from django.core.management.base import BaseCommand
from cms.models import SiteSettings, Program, Service, Testimonial, RichPage


ABOUT_TEXT = (
    "Magma7 Fitness Center is more than just a gym. We are a community dedicated to promoting a healthy and active lifestyle for everyone. "
    "Our center is located in the heart of Kaduna at No. 30 Zakaria Maimalari Street, Nasfat Layout, and is open to people of all ages and fitness levels."
)


class Command(BaseCommand):
    help = 'Seed CMS content and site settings.'

    def handle(self, *args, **options):
        settings_obj, _ = SiteSettings.objects.get_or_create(
            id=1,
            defaults=dict(
                brand_name='Magma7Fitness',
                tagline='Healthy body, healthy mind',
                phone='+234 000 000 0000',
                email='info@magma7fitness.com',
                address='No. 30 Zakaria Maimalari Street, Nasfat Layout, Kaduna',
                hero_headline='Get Healthy Body with the Perfect Exercises',
                hero_subtext='We are here to help you make a healthy body and mind through fitness.',
                hero_cta_text='Get Started',
                hero_cta_url='/memberships/plans/',
                hero_image_url='https://images.unsplash.com/photo-1554284126-aa88f22d8b74?q=80&w=1400&auto=format&fit=crop',
            )
        )

        Program.objects.get_or_create(title='Strength Training', defaults=dict(description='Programs to gain strength', icon='fitness_center', order=1))
        Program.objects.get_or_create(title='Basic Yoga', defaults=dict(description='Combine yoga with cardio', icon='self_improvement', order=2))
        Program.objects.get_or_create(title='Body Building', defaults=dict(description='Increase muscle mass and strength', icon='sports_mma', order=3))
        Program.objects.get_or_create(title='Weight Loss', defaults=dict(description='Sustainable lifestyle changes', icon='monitor_weight', order=4))

        Service.objects.get_or_create(title='Personal Training', defaults=dict(description='Personalized plan and progress tracking', order=1))
        Service.objects.get_or_create(title='Expert Trainers', defaults=dict(description='Certified, skilled trainers to guide you', order=2))
        Service.objects.get_or_create(title='Flexible Time', defaults=dict(description='Off-peak sessions and flexible hours', order=3))

        Testimonial.objects.get_or_create(name='Happy Member', quote='Great environment and trainers. I reached my goals!', rating=5)
        Testimonial.objects.get_or_create(name='Farhan Rio', quote='Trainers are amazing and push me to be my best.', rating=5)

        RichPage.objects.update_or_create(slug='about', defaults=dict(title='About Us', body=ABOUT_TEXT))
        self.stdout.write(self.style.SUCCESS('CMS content seeded.'))

