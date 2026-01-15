from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Q

User = get_user_model()

class Command(BaseCommand):
    help = 'Grant all view/add/change/delete permissions to existing staff users (non-superusers)'

    def handle(self, *args, **options):
        # Get all permissions for non-system apps
        perms = Permission.objects.filter(
            Q(codename__startswith='view_')
            | Q(codename__startswith='add_')
            | Q(codename__startswith='change_')
            | Q(codename__startswith='delete_')
        ).exclude(
            content_type__app_label__in=['auth', 'admin', 'contenttypes', 'sessions']
        )

        self.stdout.write(f"Found {perms.count()} permissions to assign")

        # Get all staff users (non-superusers)
        staff_users = User.objects.filter(is_staff=True, is_superuser=False)

        self.stdout.write(f"Found {staff_users.count()} staff users (non-superusers)")

        for user in staff_users:
            user.user_permissions.add(*perms)
            self.stdout.write(self.style.SUCCESS(f'✓ Assigned {perms.count()} permissions to {user.username}'))

        self.stdout.write(self.style.SUCCESS('Done! All staff users now have full permissions.'))
