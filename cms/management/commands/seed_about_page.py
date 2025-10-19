from django.core.management.base import BaseCommand
from cms.models import AboutPage, CoreValue, WhyChooseUsItem, AboutGalleryImage, AboutStatistic


class Command(BaseCommand):
    help = 'Seed the about page with sample content'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding about page data...')

        # Create AboutPage instance
        about_page, created = AboutPage.objects.get_or_create(
            id=1,
            defaults={
                'hero_title': 'About Magma7Fitness',
                'hero_subtitle': 'More than just a gym - we\'re a community dedicated to transforming lives through fitness, wellness, and support.',
                'hero_image_url': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1200',

                'story_title': 'Our Story',
                'story_content': '''Magma7 Fitness Center was founded with a simple yet powerful vision: to create a space where everyone, regardless of their fitness level, could feel welcome and supported in their health journey.

Located in the heart of Kaduna at No. 30 Zakaria Maimalari Street, Nasfat Layout, we've grown from a small local gym into a thriving fitness community. Our state-of-the-art facility boasts premium equipment for strength training, cardio, and functional fitness.

What sets us apart isn't just our equipment - it's our people. Our certified trainers and supportive community members create an environment where you can push your limits while feeling completely at home.''',
                'story_image_url': 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=800',

                'mission_title': 'Our Mission',
                'mission_content': 'To empower individuals to lead healthy and active lifestyles by providing a welcoming and inclusive environment that offers a range of fitness and wellness services.',
                'mission_icon': 'track_changes',

                'vision_title': 'Our Vision',
                'vision_content': 'To be the leading fitness center in Kaduna, known for providing exceptional facilities and services that enable our members to achieve their health and fitness goals.',
                'vision_icon': 'visibility',

                'why_choose_title': 'Why Choose Magma7Fitness',
                'why_choose_description': 'We offer more than just a place to work out - we provide a complete fitness ecosystem designed for your success.',

                'gallery_title': 'Our World-Class Facility',
                'gallery_description': 'Take a virtual tour of our state-of-the-art gym and see why members love training with us.',

                'cta_title': 'Ready to Transform Your Life?',
                'cta_description': 'Join thousands of satisfied members who have achieved their fitness goals with us',
                'cta_button_text': 'Start Your Journey',
                'cta_button_url': '/memberships/plans/',
                'cta_image_url': 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=1200',
            }
        )
        self.stdout.write(self.style.SUCCESS(f'✓ AboutPage {"created" if created else "already exists"}'))

        # Create Core Values
        core_values_data = [
            {
                'title': 'Health & Wellness',
                'description': 'We prioritize the health and wellness of our members and aim to promote healthy lifestyles through our services and facilities.',
                'icon': 'favorite',
                'order': 1
            },
            {
                'title': 'Inclusivity',
                'description': 'We believe in creating an inclusive environment that welcomes individuals from all backgrounds and fitness levels.',
                'icon': 'diversity_3',
                'order': 2
            },
            {
                'title': 'Excellence',
                'description': 'We strive for excellence in everything we do, from the quality of our equipment and facilities to the professionalism of our staff.',
                'icon': 'star',
                'order': 3
            },
            {
                'title': 'Community',
                'description': 'We foster a sense of community among our members and staff, promoting mutual support and encouragement.',
                'icon': 'groups',
                'order': 4
            },
            {
                'title': 'Innovation',
                'description': 'We embrace innovation in our approach to fitness and wellness, constantly seeking new and effective ways to help our members achieve their goals.',
                'icon': 'lightbulb',
                'order': 5
            },
            {
                'title': 'Integrity',
                'description': 'We operate with honesty, transparency, and accountability in all our interactions with members and partners.',
                'icon': 'verified',
                'order': 6
            },
        ]

        for data in core_values_data:
            obj, created = CoreValue.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created CoreValue: {data["title"]}'))

        # Create Why Choose Us Items
        why_choose_data = [
            {
                'title': 'Expert Trainers',
                'description': 'Our certified personal trainers are dedicated to providing personalized support and guidance throughout your fitness journey.',
                'icon': 'school',
                'order': 1
            },
            {
                'title': 'State-of-the-Art Equipment',
                'description': 'Access premium cardio and strength training equipment from leading brands, maintained to the highest standards.',
                'icon': 'fitness_center',
                'order': 2
            },
            {
                'title': 'Diverse Class Options',
                'description': 'From yoga and Pilates to Zumba and kickboxing, we offer group fitness classes for all interests and levels.',
                'icon': 'sports_gymnastics',
                'order': 3
            },
            {
                'title': 'Flexible Membership',
                'description': 'Choose from a variety of membership plans designed to fit your schedule and budget.',
                'icon': 'calendar_today',
                'order': 4
            },
            {
                'title': 'Women-Only Studio',
                'description': 'We provide a private, comfortable space for women who prefer a more intimate workout environment.',
                'icon': 'woman',
                'order': 5
            },
            {
                'title': 'Nutrition Support',
                'description': 'Healthy juice bar and nutritional guidance to complement your fitness routine and accelerate results.',
                'icon': 'restaurant',
                'order': 6
            },
        ]

        for data in why_choose_data:
            obj, created = WhyChooseUsItem.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created WhyChooseUsItem: {data["title"]}'))

        # Create Gallery Images
        gallery_data = [
            {
                'title': 'Cardio Zone',
                'description': 'Premium treadmills, ellipticals, and bikes',
                'image_url': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600',
                'order': 1
            },
            {
                'title': 'Weight Training Area',
                'description': 'Complete range of free weights and machines',
                'image_url': 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=600',
                'order': 2
            },
            {
                'title': 'Group Fitness Studio',
                'description': 'Spacious studio for classes and training',
                'image_url': 'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600',
                'order': 3
            },
            {
                'title': 'Functional Training Zone',
                'description': 'Dedicated space for functional fitness',
                'image_url': 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600',
                'order': 4
            },
            {
                'title': 'Yoga & Pilates Studio',
                'description': 'Peaceful space for mind-body workouts',
                'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600',
                'order': 5
            },
            {
                'title': 'Juice Bar',
                'description': 'Healthy refreshments and snacks',
                'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600',
                'order': 6
            },
        ]

        for data in gallery_data:
            obj, created = AboutGalleryImage.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created Gallery Image: {data["title"]}'))

        # Create Statistics
        stats_data = [
            {
                'label': 'Active Members',
                'value': '5,000+',
                'icon': 'people',
                'order': 1
            },
            {
                'label': 'Expert Trainers',
                'value': '25+',
                'icon': 'school',
                'order': 2
            },
            {
                'label': 'Years of Excellence',
                'value': '10+',
                'icon': 'emoji_events',
                'order': 3
            },
            {
                'label': 'Success Stories',
                'value': '2,500+',
                'icon': 'trending_up',
                'order': 4
            },
        ]

        for data in stats_data:
            obj, created = AboutStatistic.objects.get_or_create(
                label=data['label'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created Statistic: {data["label"]}'))

        self.stdout.write(self.style.SUCCESS('\n✅ About page seeded successfully!'))
        self.stdout.write(self.style.WARNING('\n📝 You can now edit all content from the Django admin panel.'))
