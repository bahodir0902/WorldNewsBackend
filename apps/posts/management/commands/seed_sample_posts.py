from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.posts.models import Post, PostCategory


class Command(BaseCommand):
    help = 'Create sample posts for testing'

    def handle(self, *args, **options):
        # Get or create categories
        news_cat, _ = PostCategory.objects.get_or_create(
            name='News',
            defaults={'type': PostCategory.CategoryType.NEWS, 'description': 'General news'}
        )

        announcement_cat, _ = PostCategory.objects.get_or_create(
            name='Official Announcements',
            defaults={'type': PostCategory.CategoryType.ANNOUNCEMENT}
        )

        media_cat, _ = PostCategory.objects.get_or_create(
            name='Videos',
            defaults={'type': PostCategory.CategoryType.MEDIA}
        )

        report_cat, _ = PostCategory.objects.get_or_create(
            name='Reports',
            defaults={'type': PostCategory.CategoryType.REPORT}
        )

        # Sample news posts
        news_posts = [
            {
                'title': 'New digital literacy training programs launched',
                'short_description': 'Comprehensive digital literacy programs now available for all citizens',
                'content': 'The government has launched new digital literacy training programs aimed at improving digital skills across all age groups. The programs include basic computer skills, internet safety, and advanced digital tools training.',
                'type_tag': 'Education',
                'category': news_cat,
            },
            {
                'title': 'International cultural festival to take place in March 2026',
                'short_description': 'Annual cultural festival brings together diverse communities',
                'content': 'The international cultural festival will showcase art, music, and traditions from around the world. The event is scheduled for March 2026 and will feature performances, exhibitions, and cultural workshops.',
                'type_tag': 'Culture',
                'category': news_cat,
            },
            {
                'title': 'Innovative technologies showcased at research laboratory',
                'short_description': 'Latest technological innovations presented to the public',
                'content': 'The national research laboratory opened its doors to showcase cutting-edge technological innovations. Visitors can explore advancements in artificial intelligence, renewable energy, and biotechnology.',
                'type_tag': 'Technology',
                'category': news_cat,
            },
            {
                'title': 'New entrepreneurship programs announced for youth',
                'short_description': 'Supporting young entrepreneurs with new initiatives',
                'content': 'New entrepreneurship programs have been announced to support young people in starting their own businesses. The programs include mentorship, funding opportunities, and business training.',
                'type_tag': 'Entrepreneurship',
                'category': news_cat,
            },
        ]

        # Sample announcements
        announcement_posts = [
            {
                'title': 'Grand opening ceremony of new research center',
                'short_description': 'State-of-the-art research facility opens its doors',
                'content': 'The grand opening ceremony of the new research center will take place on January 7, 2026. The facility will focus on advanced scientific research and innovation.',
                'type_tag': 'Events',
                'category': announcement_cat,
            },
            {
                'title': 'Free online courses announced for citizens',
                'short_description': 'Access to quality education for everyone',
                'content': 'Free online courses are now available covering various subjects including technology, business, languages, and personal development. Registration is open to all citizens.',
                'type_tag': 'Education',
                'category': announcement_cat,
            },
        ]

        # Sample videos
        video_posts = [
            {
                'title': 'Effective use of digital technologies',
                'short_description': 'Learn how to effectively use digital tools',
                'content': 'This video tutorial covers best practices for using digital technologies in daily life and work.',
                'type_tag': 'Tutorial',
                'category': media_cat,
                'video_url': 'https://www.youtube.com/watch?v=example',
            },
            {
                'title': 'About the center\'s activities and mission',
                'short_description': 'Discover our mission and ongoing activities',
                'content': 'An overview of our center\'s mission, vision, and the various programs we offer to the community.',
                'type_tag': 'About',
                'category': media_cat,
                'video_url': 'https://www.youtube.com/watch?v=example2',
            },
        ]

        all_posts = news_posts + announcement_posts + video_posts

        created_count = 0
        now = timezone.now()

        for i, post_data in enumerate(all_posts):
            # Create post with published status and staggered dates
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    **post_data,
                    'status': Post.Status.PUBLISHED,
                    'published_at': now - timedelta(days=i),
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created post: {post.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Post already exists: {post.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal posts created: {created_count}')
        )

