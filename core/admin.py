"""
Unfold Admin Configuration
https://unfoldadmin.com/docs/
"""

from django.contrib.admin import AdminSite
from unfold.admin import ModelAdmin


class UnfoldAdminSite(AdminSite):
    """Custom admin site with Unfold integration"""
    title = "World News Admin"
    site_title = "World News"
    site_header = "World News Administration"
    index_title = "Dashboard"

    def get_app_list(self, request):
        """Customize app list order and grouping"""
        app_list = super().get_app_list(request)

        # Reorder apps
        app_order = {
            'posts': 0,
            'logs': 1,
            'auth': 2,
        }

        app_list.sort(key=lambda x: app_order.get(x['app_label'], 999))
        return app_list


# Create instance for registration
unfold_admin_site = UnfoldAdminSite()


class UnfoldBaseAdmin(ModelAdmin):
    """Base admin class for all models with common Unfold settings"""

    def get_readonly_fields(self, request, obj=None):
        """Add created_at and updated_at to readonly"""
        readonly = list(self.readonly_fields) if self.readonly_fields else []
        if hasattr(self.model, 'created_at'):
            if 'created_at' not in readonly:
                readonly.append('created_at')
        if hasattr(self.model, 'updated_at'):
            if 'updated_at' not in readonly:
                readonly.append('updated_at')
        return readonly

