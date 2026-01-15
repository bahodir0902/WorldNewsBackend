from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from apps.logs.models import LogEntry


class LogEntryAdmin(ModelAdmin):
    """Enhanced admin for LogEntry with Unfold"""

    list_display = [
        'timestamp_display',
        'level_badge',
        'logger_name_display',
        'message_preview',
    ]

    list_filter = [
        'level',
        'logger_name',
        'timestamp',
    ]

    search_fields = ['message', 'logger_name', 'pathname']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp', 'level', 'logger_name', 'message', 'pathname', 'line_no', 'exception']
    date_hierarchy = 'timestamp'

    fieldsets = (
        ('⏰ Timing', {
            'fields': ('timestamp',),
        }),
        ('📋 Log Details', {
            'fields': ('level', 'logger_name', 'message'),
        }),
        ('🔍 Location', {
            'fields': ('pathname', 'line_no'),
            'classes': ('collapse',),
        }),
        ('⚠️ Exception', {
            'fields': ('exception',),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        """Logs are read-only"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Allow deletion of old logs"""
        return True

    @display(
        description='Timestamp',
        ordering='timestamp',
    )
    def timestamp_display(self, obj):
        """Display timestamp in readable format"""
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    @display(
        description='Level',
        ordering='level',
    )
    def level_badge(self, obj):
        """Display log level as colored badge"""
        level_colors = {
            'INFO': '#3B82F6',      # Blue
            'WARNING': '#F59E0B',   # Amber
            'ERROR': '#EF4444',     # Red
            'DEBUG': '#8B5CF6',     # Purple
            'CRITICAL': '#DC2626',  # Dark Red
        }

        level_emojis = {
            'INFO': 'ℹ️',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'DEBUG': '🐛',
            'CRITICAL': '🔥',
        }

        color = level_colors.get(obj.level, '#6B7280')
        emoji = level_emojis.get(obj.level, '📌')

        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 8px; font-weight: 500; font-size: 12px; white-space: nowrap;">'
            '{} {}</span>',
            color,
            emoji,
            obj.level
        )

    @display(
        description='Logger',
        ordering='logger_name',
    )
    def logger_name_display(self, obj):
        """Display logger name shortened"""
        parts = obj.logger_name.split('.')
        if len(parts) > 2:
            return '.'.join(parts[-2:])
        return obj.logger_name

    @display(
        description='Message',
        ordering='message',
    )
    def message_preview(self, obj):
        """Display message preview"""
        message = obj.message.replace('\n', ' ')
        if len(message) > 80:
            return message[:77] + '...'
        return message


admin.site.register(LogEntry, LogEntryAdmin)

