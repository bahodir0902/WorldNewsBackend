from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Q

class Command(BaseCommand):
    help = 'Assign view_ and change_ permissions for non-system apps to staff users (non-superusers)'

    def handle(self, *args, **options):
        User = get_user_model()
        perms = Permission.objects.filter(
            Q(codename__startswith='view_') | Q(codename__startswith='change_')
        ).exclude(content_type__app_label__in=['auth', 'admin', 'contenttypes', 'sessions'])

        users = User.objects.filter(is_staff=True, is_superuser=False)
        for u in users:
            before = u.user_permissions.count()
            u.user_permissions.add(*perms)
            after = u.user_permissions.count()
            self.stdout.write(self.style.SUCCESS(f'Updated {u.username}: {before} -> {after} perms'))

        self.stdout.write(self.style.SUCCESS('Done.'))
