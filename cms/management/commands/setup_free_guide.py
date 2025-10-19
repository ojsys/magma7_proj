from django.core.management.base import BaseCommand
from cms.models import SiteSettings


class Command(BaseCommand):
    help = 'Setup free guide settings'

    def handle(self, *args, **options):
        settings, created = SiteSettings.objects.get_or_create(pk=1)

        # Update free guide settings
        settings.free_guide_title = "Complete Fitness Transformation Guide"
        settings.free_guide_description = "A comprehensive 30-page guide covering workout routines, nutrition tips, and goal-setting strategies for beginners to advanced fitness enthusiasts."
        settings.free_guide_text = "Download Free"
        settings.free_guide_url = "https://example.com/free-fitness-guide.pdf"  # You can replace this with your actual PDF URL

        settings.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully set up free guide settings')
        )
        self.stdout.write(f"Guide Title: {settings.free_guide_title}")
        self.stdout.write(f"Guide URL: {settings.free_guide_url}")
        self.stdout.write(f"Button Text: {settings.free_guide_text}")