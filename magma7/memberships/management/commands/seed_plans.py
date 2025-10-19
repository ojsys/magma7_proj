from django.core.management.base import BaseCommand
from memberships.models import Plan
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create sample membership plans (idempotent)'

    def handle(self, *args, **options):
        samples = [
            {
                'name': 'Monthly',
                'description': '30-day access to all facilities and classes.',
                'price': Decimal('15000.00'),
                'duration_days': 30,
            },
            {
                'name': 'Quarterly',
                'description': '90-day access at a discounted rate.',
                'price': Decimal('40000.00'),
                'duration_days': 90,
            },
            {
                'name': 'Annual',
                'description': '365-day full access with best value.',
                'price': Decimal('140000.00'),
                'duration_days': 365,
            },
        ]
        created = 0
        for s in samples:
            obj, was_created = Plan.objects.update_or_create(
                name=s['name'],
                defaults={
                    'description': s['description'],
                    'price': s['price'],
                    'duration_days': s['duration_days'],
                    'is_active': True,
                }
            )
            created += 1 if was_created else 0
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(samples)} plans ({created} new).'))
