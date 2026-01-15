from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from unfold.admin import ModelAdmin
from django.utils.translation import gettext_lazy as _
from django import forms
from django.db.models import Q

# Unregister default Group model (hide Groups/Permissions as requested)
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# Unregister default User model to replace it
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for creating users with enhanced password widgets (Unfold).
    New users are staff by default to have equal rights as superusers.
    is_superuser is completely hidden (superusers only via manage.py createsuperuser).
    """
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'vTextField unfold-password-field',
                'autocomplete': 'new-password',
            }
        ),
        help_text=UserCreationForm.base_fields['password1'].help_text,
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'vTextField unfold-password-field',
                'autocomplete': 'new-password',
            }
        ),
        help_text=_("Enter the same password for verification."),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_staff", "is_active")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default new users to staff=True so they have equal rights
        self.fields['is_staff'].initial = True
        self.fields['is_staff'].help_text = _("Designates whether the user can log into this admin site.")


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """
    Admin interface for Django's built-in User model.
    - New users are staff by default (equal rights as superusers)
    - is_superuser is hidden (superusers created only via manage.py createsuperuser)
    - Groups and Permissions fields are hidden
    - Superusers cannot be deleted via admin
    - Newly created users automatically receive all permissions (view/add/change/delete)
    """
    form = BaseUserAdmin.form
    add_form = CustomUserCreationForm

    # Unfold UI enhancements
    compressed_fields = True
    warn_unsaved_form = True

    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active", "is_superuser")
    list_filter = ("is_staff", "is_active", "is_superuser", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    # Change form fieldsets - hide is_superuser, password, groups, and user_permissions
    fieldsets = (
        (_("User Profile"), {
            "fields": ("username", "first_name", "last_name", "email"),
        }),
        (_("Permissions & Status"), {
            "fields": ("is_active", "is_staff"),
        }),
        (_("Important dates"), {
            "fields": ("last_login", "date_joined"),
            "classes": ("collapse",),
        }),
    )

    # Creation form fieldsets - only essential fields
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "first_name", "last_name", "email", "is_staff", "is_active"),
        }),
    )

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of superusers."""
        if obj and obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        """
        Save the user and automatically grant all permissions to newly created staff users.
        """
        super().save_model(request, obj, form, change)

        # If this is a new user (not an edit) and is staff, grant all permissions
        if not change and obj.is_staff and not obj.is_superuser:
            # Get all permissions excluding system apps
            perms = Permission.objects.filter(
                Q(codename__startswith='view_')
                | Q(codename__startswith='add_')
                | Q(codename__startswith='change_')
                | Q(codename__startswith='delete_')
            ).exclude(
                content_type__app_label__in=['auth', 'admin', 'contenttypes', 'sessions']
            )
            obj.user_permissions.add(*perms)

