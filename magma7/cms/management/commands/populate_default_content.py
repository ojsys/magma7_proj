"""
Management command to populate default hero slides and visual content
"""
from django.core.management.base import BaseCommand
from cms.models import HeroSlide, Program, Service


class Command(BaseCommand):
    help = 'Populates default hero slides and visual content for the home page'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating default content...'))

        # Create default hero slides
        hero_slides_data = [
            {
                'title': 'Modern Gym Equipment',
                'image_url': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2000&auto=format&fit=crop',
                'order': 0,
            },
            {
                'title': 'Personal Training Session',
                'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?q=80&w=2000&auto=format&fit=crop',
                'order': 1,
            },
            {
                'title': 'Group Fitness Class',
                'image_url': 'https://images.unsplash.com/photo-1518611012118-696072aa579a?q=80&w=2000&auto=format&fit=crop',
                'order': 2,
            },
            {
                'title': 'Cardio Training',
                'image_url': 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?q=80&w=2000&auto=format&fit=crop',
                'order': 3,
            },
            {
                'title': 'Weight Training',
                'image_url': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=2000&auto=format&fit=crop',
                'order': 4,
            },
        ]

        created_slides = 0
        for slide_data in hero_slides_data:
            slide, created = HeroSlide.objects.get_or_create(
                title=slide_data['title'],
                defaults={
                    'image_url': slide_data['image_url'],
                    'order': slide_data['order'],
                    'is_active': True,
                }
            )
            if created:
                created_slides += 1
                self.stdout.write(f'  ✓ Created hero slide: {slide.title}')
            else:
                self.stdout.write(f'  - Hero slide already exists: {slide.title}')

        self.stdout.write(self.style.SUCCESS(f'\nCreated {created_slides} hero slides'))

        # Update programs with icons if they exist
        program_icons = {
            'Strength Training': 'fitness_center',
            'Cardio': 'directions_run',
            'Yoga': 'self_improvement',
            'HIIT': 'local_fire_department',
            'CrossFit': 'sports_martial_arts',
            'Pilates': 'accessibility_new',
            'Functional Training': 'sports_gymnastics',
            'Personal Training': 'person',
        }

        updated_programs = 0
        for program_name, icon in program_icons.items():
            programs = Program.objects.filter(title__icontains=program_name.split()[0])
            for program in programs:
                if not program.icon:
                    program.icon = icon
                    program.save()
                    updated_programs += 1
                    self.stdout.write(f'  ✓ Updated program icon: {program.title}')

        if updated_programs > 0:
            self.stdout.write(self.style.SUCCESS(f'\nUpdated {updated_programs} program icons'))

        self.stdout.write(self.style.SUCCESS('\n✨ Default content population complete!'))
        self.stdout.write(self.style.WARNING('\nNote: Hero slides will now appear on the home page.'))
        self.stdout.write(self.style.WARNING('You can manage them at: /admin/cms/heroslide/'))
