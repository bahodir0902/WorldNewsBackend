"""
Structured Logging Utility for Admin Operations
Provides readable, formatted logging for all write operations
"""

import logging
from django.contrib.auth.models import User
from django.utils import timezone
from typing import Optional, Dict, Any

logger = logging.getLogger('django')


class AdminLogger:
    """Structured logging for admin operations"""

    COLORS = {
        'CREATED': '[CREATED]',
        'UPDATED': '[UPDATED]',
        'DELETED': '[DELETED]',
        'ACTION': '[ACTION]',
    }

    @staticmethod
    def log_action(
        action: str,
        model_name: str,
        instance: Any,
        user: User,
        changes: Optional[Dict] = None,
        extra_info: Optional[str] = None
    ):
        """
        Log an admin action in a readable format

        Args:
            action: 'CREATED', 'UPDATED', 'DELETED', or custom action name
            model_name: Name of the model (e.g., 'Post', 'PostCategory')
            instance: The model instance
            user: The user who performed the action
            changes: Dictionary of field changes {field: (old_value, new_value)}
            extra_info: Additional information to log
        """

        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        emoji = AdminLogger.COLORS.get(action, '[ACTION]')
        user_display = f"{user.first_name} {user.last_name}" if user.first_name else user.username

        # Build the log message
        log_lines = [
            f"\n{'='*80}",
            f"{emoji} {action.upper()} | {model_name}",
            f"{'='*80}",
            f"Timestamp: {timestamp}",
            f"User: {user_display} ({user.email})",
            f"ID: {instance.pk}",
        ]

        # Add instance representation
        if hasattr(instance, 'title'):
            log_lines.append(f"Title: {instance.title}")
        elif hasattr(instance, 'name'):
            log_lines.append(f"Name: {instance.name}")

        if hasattr(instance, 'slug'):
            log_lines.append(f"Slug: {instance.slug}")

        if hasattr(instance, 'status'):
            log_lines.append(f"Status: {instance.status}")

        if hasattr(instance, 'published_at'):
            pub_at = instance.published_at
            log_lines.append(f"Published: {pub_at.strftime('%Y-%m-%d %H:%M:%S') if pub_at else 'Not published'}")

        # Add changes if provided
        if changes and action == 'UPDATED':
            log_lines.append(f"\nChanges:")
            for field, (old_value, new_value) in changes.items():
                log_lines.append(f"  • {field}:")
                log_lines.append(f"      Old: {AdminLogger._format_value(old_value)}")
                log_lines.append(f"      New: {AdminLogger._format_value(new_value)}")

        # Add extra info
        if extra_info:
            log_lines.append(f"\nInfo: {extra_info}")

        log_lines.append(f"{'='*80}\n")

        message = '\n'.join(log_lines)
        logger.info(message)

        return message

    @staticmethod
    def _format_value(value: Any) -> str:
        """Format a value for logging"""
        if value is None:
            return "None"
        elif isinstance(value, bool):
            return "Yes" if value else "No"
        elif isinstance(value, (list, tuple)):
            return f"[{len(value)} items]"
        elif isinstance(value, dict):
            return f"{{...}} ({len(value)} keys)"
        elif len(str(value)) > 50:
            return f"{str(value)[:47]}..."
        else:
            return str(value)

    @staticmethod
    def log_bulk_action(
        action: str,
        model_name: str,
        count: int,
        user: User,
        query_description: Optional[str] = None
    ):
        """Log bulk operations like delete/status change"""

        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        emoji = AdminLogger.COLORS.get(action, '[ACTION]')
        user_display = f"{user.first_name} {user.last_name}" if user.first_name else user.username

        log_lines = [
            f"\n{'='*80}",
            f"{emoji} BULK {action.upper()} | {model_name}",
            f"{'='*80}",
            f"Timestamp: {timestamp}",
            f"User: {user_display} ({user.email})",
            f"Items Affected: {count}",
        ]

        if query_description:
            log_lines.append(f"Query: {query_description}")

        log_lines.append(f"{'='*80}\n")

        message = '\n'.join(log_lines)
        logger.info(message)

        return message


def log_admin_change(sender, instance, created, **kwargs):
    """
    Signal handler for post_save to log changes
    Connect this to: post_save.connect(log_admin_change, sender=YourModel)
    """
    # This is handled in the admin class itself
    pass


def compare_model_fields(old_instance: Any, new_instance: Any) -> Dict[str, tuple]:
    """
    Compare two model instances and return changed fields

    Returns:
        Dict of {field_name: (old_value, new_value)}
    """
    changes = {}

    if old_instance is None:
        return changes

    # Get all fields from the model
    for field in new_instance._meta.get_fields():
        if field.name in ('created_at', 'updated_at', 'id', 'is_deleted'):
            continue

        try:
            old_value = getattr(old_instance, field.name)
            new_value = getattr(new_instance, field.name)

            # Compare values
            if old_value != new_value:
                changes[field.name] = (old_value, new_value)
        except AttributeError:
            continue

    return changes

