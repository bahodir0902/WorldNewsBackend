# flake8: noqa
import logging

from celery import shared_task
from decouple import config
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)
TTL_SECONDS = config("TTL_SECONDS", cast=int, default=300)
TTL_MINUTES = TTL_SECONDS // 60

# Premium Brand Colors - Minimalist & Elegant
BRAND_COLORS = {
    "white": "#FFFFFF",
    "black": "#000000",
    "gray_50": "#FAFAFA",
    "gray_100": "#F5F5F5",
    "gray_200": "#E5E5E5",
    "gray_300": "#D4D4D4",
    "gray_400": "#A3A3A3",
    "gray_600": "#525252",
    "gray_700": "#404040",
    "gray_800": "#262626",
    "gray_900": "#171717",
}


def get_email_base_template(title, content, footer_text=None):
    """
    Premium minimalist base template for all emails
    """
    footer = footer_text or "If you didn't request this, please ignore this message."

    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body style="margin:0;padding:0;background:{BRAND_COLORS['gray_50']};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;">
    <div style="max-width:600px;margin:0 auto;padding:40px 20px;">

        <!-- Brand Header -->
        <div style="text-align:center;margin-bottom:48px;">
            <div style="display:inline-block;padding:12px 24px;background:{BRAND_COLORS['black']};border-radius:4px;">
                <h1 style="font-size:20px;font-weight:600;color:{BRAND_COLORS['white']};margin:0;letter-spacing:-0.5px;">
                    YOUR BRAND
                </h1>
            </div>
        </div>

        <!-- Main Card -->
        <div style="background:{BRAND_COLORS['white']};border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.1),0 1px 2px rgba(0,0,0,0.06);">

            <!-- Content Header -->
            <div style="padding:40px 40px 32px;border-bottom:1px solid {BRAND_COLORS['gray_200']};">
                <h2 style="color:{BRAND_COLORS['black']};margin:0;font-size:28px;font-weight:600;letter-spacing:-0.5px;line-height:1.2;">
                    {title}
                </h2>
            </div>

            <!-- Main Content -->
            <div style="padding:40px;">
                {content}
            </div>

            <!-- Footer -->
            <div style="background:{BRAND_COLORS['gray_50']};padding:32px 40px;border-top:1px solid {BRAND_COLORS['gray_200']};">
                <p style="margin:0 0 16px;font-size:14px;line-height:1.6;color:{BRAND_COLORS['gray_600']};text-align:center;">
                    {footer}
                </p>
                <p style="margin:0;font-size:13px;color:{BRAND_COLORS['gray_600']};text-align:center;">
                    Need help? <a href="mailto:support@yourbrand.com" style="color:{BRAND_COLORS['black']};text-decoration:none;font-weight:500;border-bottom:1px solid {BRAND_COLORS['gray_300']};">Contact Support</a>
                </p>
            </div>
        </div>

        <!-- Bottom Footer -->
        <div style="text-align:center;margin-top:32px;padding:0 20px;">
            <p style="margin:0 0 8px;font-size:13px;color:{BRAND_COLORS['gray_600']};line-height:1.6;">
                <strong style="color:{BRAND_COLORS['black']};font-weight:600;">Your Brand Team</strong>
            </p>
            <a href="https://yourbrand.com/" style="display:inline-block;margin-top:8px;font-size:13px;color:{BRAND_COLORS['gray_600']};text-decoration:none;border-bottom:1px solid {BRAND_COLORS['gray_300']};">
                yourbrand.com
            </a>
        </div>
    </div>
</body>
</html>"""


@shared_task(bind=True, max_retries=3)
def send_email_verification_task(self, receiver_email, first_name, code):
    """
    Celery task to send email verification with premium minimalist design
    """
    try:
        subject = "Verify Your Email Address"
        from_email = config("EMAIL_HOST_USER")
        to = [receiver_email]

        text_content = f"""
Hello {first_name},

Thank you for signing up! To protect your account, please verify your email address.

Your 4-digit verification code: {code}

Enter this code on our website to complete the verification process.

If you didn't request this, please ignore this message.

Best regards,
Your Brand Team
        """

        content = f"""
            <p style="margin:0 0 8px;font-size:16px;line-height:1.6;color:{BRAND_COLORS['gray_900']};">
                Hello <strong style="color:{BRAND_COLORS['black']};font-weight:600;">{first_name}</strong>,
            </p>
            <p style="margin:0 0 32px;font-size:15px;line-height:1.6;color:{BRAND_COLORS['gray_700']};">
                Thank you for signing up! To protect your account, please verify your email address.
            </p>

            <!-- Code Display -->
            <div style="background:{BRAND_COLORS['gray_50']};border:2px solid {BRAND_COLORS['black']};border-radius:8px;padding:32px;margin:32px 0;text-align:center;">
                <p style="margin:0 0 16px;font-size:11px;color:{BRAND_COLORS['gray_600']};text-transform:uppercase;letter-spacing:1.5px;font-weight:600;">
                    Verification Code
                </p>
                <div style="font-family:'SF Mono',Monaco,Consolas,'Courier New',monospace;font-size:42px;font-weight:700;color:{BRAND_COLORS['black']};letter-spacing:8px;">
                    {code}
                </div>
            </div>

            <p style="margin:0;font-size:14px;line-height:1.6;color:{BRAND_COLORS['gray_700']};text-align:center;">
                Enter this code on our website to complete the verification process.
            </p>
        """

        html_content = get_email_base_template("Verify Your Email", content)

        email = EmailMultiAlternatives(subject, text_content, from_email, to)
        email.attach_alternative(html_content, "text/html")
        email.send()

        logger.info(f"Email verification sent successfully to {receiver_email}")
        return f"Email sent to {receiver_email}"

    except Exception as exc:
        logger.error(f"Failed to send email verification to {receiver_email}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_password_verification_task(self, email, first_name, code):
    """
    Celery task to send password reset verification with premium minimalist design
    """
    try:
        subject = "Reset Your Password"
        to = [email]
        from_email = config("EMAIL_HOST_USER")

        text_content = f"""
Hello {first_name},

We received a request to reset your account password.

Your 4-digit password reset code: {code}

Enter this code on our website to set a new password.

If you didn't request a password reset, please ignore this message.

Best regards,
Your Brand Team
        """

        content = f"""
            <p style="margin:0 0 8px;font-size:16px;line-height:1.6;color:{BRAND_COLORS['gray_900']};">
                Hello <strong style="color:{BRAND_COLORS['black']};font-weight:600;">{first_name}</strong>,
            </p>
            <p style="margin:0 0 32px;font-size:15px;line-height:1.6;color:{BRAND_COLORS['gray_700']};">
                We received a request to reset your account password. For your security, please keep this code confidential.
            </p>

            <!-- Code Display -->
            <div style="background:{BRAND_COLORS['gray_50']};border:2px solid {BRAND_COLORS['black']};border-radius:8px;padding:32px;margin:32px 0;text-align:center;">
                <p style="margin:0 0 16px;font-size:11px;color:{BRAND_COLORS['gray_600']};text-transform:uppercase;letter-spacing:1.5px;font-weight:600;">
                    Password Reset Code
                </p>
                <div style="font-family:'SF Mono',Monaco,Consolas,'Courier New',monospace;font-size:42px;font-weight:700;color:{BRAND_COLORS['black']};letter-spacing:8px;">
                    {code}
                </div>
            </div>

            <div style="background:{BRAND_COLORS['gray_100']};border-left:3px solid {BRAND_COLORS['black']};padding:16px 20px;margin:32px 0;border-radius:4px;">
                <p style="margin:0;font-size:13px;line-height:1.6;color:{BRAND_COLORS['gray_700']};">
                    <strong style="color:{BRAND_COLORS['black']};font-weight:600;">Security Notice:</strong> Never share this code with anyone. This code is valid for a limited time only.
                </p>
            </div>

            <p style="margin:0;font-size:14px;line-height:1.6;color:{BRAND_COLORS['gray_700']};text-align:center;">
                Enter this code on our website to set a new password.
            </p>
        """

        html_content = get_email_base_template("Password Reset", content)

        email_msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        logger.info(f"Password reset email sent successfully to {email}")
        return f"Password reset email sent to {email}"

    except Exception as exc:
        logger.error(f"Failed to send password reset email to {email}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_email_change_verification_task(self, receiver_new_email, first_name, code):
    """
    Celery task to send email change verification with premium minimalist design
    """
    try:
        subject = "Verify Your New Email Address"
        from_email = config("EMAIL_HOST_USER")
        to = [receiver_new_email]

        text_content = f"""
Hello {first_name},

We received a request to change the email address associated with your account.

To verify your new email address, please enter the following 4-digit code:

{code}

If you didn't request this change, please ignore this message.

Best regards,
Your Brand Team
        """

        content = f"""
            <p style="margin:0 0 8px;font-size:16px;line-height:1.6;color:{BRAND_COLORS['gray_900']};">
                Hello <strong style="color:{BRAND_COLORS['black']};font-weight:600;">{first_name}</strong>,
            </p>
            <p style="margin:0 0 32px;font-size:15px;line-height:1.6;color:{BRAND_COLORS['gray_700']};">
                We received a request to change the email address associated with your account. To continue, please enter the code below.
            </p>

            <!-- Code Display -->
            <div style="background:{BRAND_COLORS['gray_50']};border:2px solid {BRAND_COLORS['black']};border-radius:8px;padding:32px;margin:32px 0;text-align:center;">
                <p style="margin:0 0 16px;font-size:11px;color:{BRAND_COLORS['gray_600']};text-transform:uppercase;letter-spacing:1.5px;font-weight:600;">
                    Verification Code
                </p>
                <div style="font-family:'SF Mono',Monaco,Consolas,'Courier New',monospace;font-size:42px;font-weight:700;color:{BRAND_COLORS['black']};letter-spacing:8px;">
                    {code}
                </div>
            </div>

            <p style="margin:0;font-size:14px;line-height:1.6;color:{BRAND_COLORS['gray_700']};text-align:center;">
                Enter this code on our website to verify your new email address.
            </p>
        """

        html_content = get_email_base_template("Email Change", content)

        email = EmailMultiAlternatives(subject, text_content, from_email, to)
        email.attach_alternative(html_content, "text/html")
        email.send()

        logger.info(f"Email change verification sent successfully to {receiver_new_email}")
        return f"Email change verification sent to {receiver_new_email}"

    except Exception as exc:
        logger.error(
            f"Failed to send email change verification to {receiver_new_email}: {str(exc)}"
        )
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_activation_invite_task(self, email, first_name, uid, token):
    """
    Celery task to send activation invite with premium minimalist design
    """
    try:
        subject = "Welcome to Your Brand"
        from_email = config("EMAIL_HOST_USER")
        frontend_url = config("FRONTEND_URL")
        activation_link = f"{frontend_url.rstrip('/')}/activate?uid={uid}&token={token}"
        to = [email]

        text_content = f"""Hello {first_name},

You've been invited to join our platform.

To get started, activate your account:
{activation_link}

If you weren't expecting this invitation, please ignore this message.

— Your Brand Team
"""

        content = f"""
            <p style="margin:0 0 8px;font-size:16px;line-height:1.6;color:{BRAND_COLORS['gray_900']};">
                Hello <strong style="color:{BRAND_COLORS['black']};font-weight:600;">{first_name}</strong>,
            </p>
            <p style="margin:0 0 32px;font-size:15px;line-height:1.6;color:{BRAND_COLORS['gray_700']};">
                You've been invited to join our platform. To get started, verify your email address and set up your account.
            </p>

            <!-- CTA Button -->
            <div style="text-align:center;margin:40px 0;">
                <a href="{activation_link}"
                   style="display:inline-block;padding:14px 32px;background:{BRAND_COLORS['black']};color:{BRAND_COLORS['white']};text-decoration:none;border-radius:6px;font-size:15px;font-weight:600;letter-spacing:-0.2px;transition:opacity 0.2s;">
                    Activate Account
                </a>
            </div>

            <!-- Link Alternative -->
            <div style="background:{BRAND_COLORS['gray_50']};padding:20px;border-radius:6px;margin:32px 0;">
                <p style="margin:0 0 8px;font-size:12px;color:{BRAND_COLORS['gray_600']};text-align:center;font-weight:500;">
                    Or copy this link to your browser:
                </p>
                <p style="margin:0;font-size:12px;color:{BRAND_COLORS['gray_700']};text-align:center;word-break:break-all;line-height:1.6;">
                    <a href="{activation_link}" style="color:{BRAND_COLORS['gray_700']};text-decoration:underline;">
                        {activation_link}
                    </a>
                </p>
            </div>
        """

        html_content = get_email_base_template(
            "Activate Your Account",
            content,
            "If you weren't expecting this invitation, please ignore this message.",
        )

        email_msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        logger.info(f"Activation invite sent successfully to {email}")
        return f"Activation invite sent to {email}"

    except Exception as exc:
        logger.error(f"Failed to send activation invite to {email}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_otp_verification_task(self, email, first_name, otp_code):
    """
    Celery task to send 2FA OTP verification with premium minimalist design
    """
    try:
        subject = "Your Sign-In Verification Code"
        from_email = config("EMAIL_HOST_USER")
        to = [email]

        text_content = f"""Hello {first_name},

Your verification code is: {otp_code}

Enter this code to complete your sign-in. This code is valid for {TTL_MINUTES} minutes.

If you didn't request this code, please ignore this message and consider changing your password.

— Your Brand Team
"""

        content = f"""
            <p style="margin:0 0 8px;font-size:16px;line-height:1.6;color:{BRAND_COLORS['gray_900']};">
                Hello <strong style="color:{BRAND_COLORS['black']};font-weight:600;">{first_name}</strong>,
            </p>
            <p style="margin:0 0 32px;font-size:15px;line-height:1.6;color:{BRAND_COLORS['gray_700']};">
                To complete your sign-in, enter the verification code below:
            </p>

            <!-- OTP Code Display -->
            <div style="background:{BRAND_COLORS['gray_50']};border:2px solid {BRAND_COLORS['black']};border-radius:8px;padding:36px;margin:32px 0;text-align:center;">
                <p style="margin:0 0 20px;font-size:11px;color:{BRAND_COLORS['gray_600']};text-transform:uppercase;letter-spacing:1.5px;font-weight:600;">
                    Verification Code
                </p>
                <div style="font-family:'SF Mono',Monaco,Consolas,'Courier New',monospace;font-size:48px;font-weight:700;color:{BRAND_COLORS['black']};letter-spacing:12px;line-height:1;">
                    {otp_code}
                </div>
            </div>

            <p style="margin:0 0 32px;font-size:14px;line-height:1.6;color:{BRAND_COLORS['gray_700']};text-align:center;">
                This code is valid for <strong style="color:{BRAND_COLORS['black']};font-weight:600;">{TTL_MINUTES} minutes</strong>
            </p>

            <!-- Security Warning -->
            <div style="background:{BRAND_COLORS['gray_100']};border-left:3px solid {BRAND_COLORS['black']};padding:16px 20px;border-radius:4px;">
                <p style="margin:0;font-size:13px;line-height:1.6;color:{BRAND_COLORS['gray_700']};">
                    <strong style="color:{BRAND_COLORS['black']};font-weight:600;">Security Tip:</strong> Never share this code with anyone. Our team will never ask for your verification code.
                </p>
            </div>
        """

        html_content = get_email_base_template(
            "Sign-In Verification",
            content,
            "If you didn't request this code, please ignore this message.",
        )

        email_msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.extra_headers = {
            "X-Priority": "1",
            "X-MSMail-Priority": "High",
        }
        email_msg.send()

        logger.info(f"OTP verification code sent successfully to {email}")
        return f"OTP verification code sent to {email}"

    except Exception as exc:
        logger.error(f"Failed to send OTP verification code to {email}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))