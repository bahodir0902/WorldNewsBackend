from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.posts.models import Post, PostCategory


class Command(BaseCommand):
    help = 'Create initial post categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'News',
                'type': PostCategory.CategoryType.NEWS,
                'description': 'General news articles'
            },
            {
                'name': 'Education',
                'type': PostCategory.CategoryType.NEWS,
                'description': 'Educational news and updates'
            },
            {
                'name': 'Technology',
                'type': PostCategory.CategoryType.NEWS,
                'description': 'Technology news'
            },
            {
                'name': 'Official Announcements',
                'type': PostCategory.CategoryType.ANNOUNCEMENT,
                'description': 'Official announcements and updates'
            },
            {
                'name': 'Events',
                'type': PostCategory.CategoryType.ANNOUNCEMENT,
                'description': 'Event announcements'
            },
            {
                'name': 'Videos',
                'type': PostCategory.CategoryType.MEDIA,
                'description': 'Video content'
            },
            {
                'name': 'Photo Gallery',
                'type': PostCategory.CategoryType.MEDIA,
                'description': 'Photo galleries and media'
            },
            {
                'name': 'Reports',
                'type': PostCategory.CategoryType.REPORT,
                'description': 'Annual and periodic reports'
            },
        ]

        created_count = 0
        for cat_data in categories:
            category, created = PostCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'type': cat_data['type'],
                    'description': cat_data['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal categories created: {created_count}')
        )

