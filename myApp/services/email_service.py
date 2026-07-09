import requests
from django.conf import settings

from django.utils import timezone
from myApp.models import EmailVerification



def send_brevo_email(to_email, subject, html_content):
    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "api-key": settings.BREVO_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "sender": {
            "name": "SJS Company",
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "to": [
            {
                "email": to_email
            }
        ],
        "subject": subject,
        "htmlContent": html_content
    }

    response = requests.post(url, json=data, headers=headers)

    return response.status_code, response.text




def send_verification_email(user, token, request):
    print("🔥 EMAIL FUNCTION CALLED")

    verify_url = request.build_absolute_uri(
        f"/verify-email/{token}/"
    )

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "api-key": settings.BREVO_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "sender": {
            "name": "SJS Company",
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "to": [
            {
                "email": user.email
            }
        ],
        "subject": "Verify your account",
        "htmlContent": f"""
            <h2>Welcome {user.first_name}</h2>
            <p>Click below to verify your account:</p>
            <a href="{verify_url}">Verify Email</a>
        """
    }

    response = requests.post(url, json=data, headers=headers)

    print("🔥 BREVO STATUS:", response.status_code)
    print("🔥 BREVO RESPONSE:", response.text)

    return response.status_code




import requests
from django.conf import settings


def send_welcome_email(user):
    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "api-key": settings.BREVO_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "sender": {
            "name": "SJS Company",
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "to": [
            {
                "email": user.email
            }
        ],
        "subject": "Welcome to SJS Company 🎉",
        "htmlContent": f"""
            <h2>Welcome {user.first_name} 👋</h2>
            <p>Your account has been successfully verified.</p>
            <p>You can now log in and start using our services.</p>
            <br>
            <p>— SJS Company Team</p>
        """
    }

    response = requests.post(url, json=data, headers=headers)

    print("🔥 WELCOME EMAIL STATUS:", response.status_code)
    print("🔥 WELCOME EMAIL RESPONSE:", response.text)

    return response.status_code



def send_password_reset_email(user, token, request):
    reset_url = request.build_absolute_uri(
        f"/reset-password/{token}/"
    )

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "api-key": settings.BREVO_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "sender": {
            "name": "SJS Company",
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "to": [
            {
                "email": user.email
            }
        ],
        "subject": "Reset Your Password",
        "htmlContent": f"""
            <h2>Hello {user.first_name}</h2>

            <p>We received a password reset request.</p>

            <p>
                <a href="{reset_url}">
                    Reset Password
                </a>
            </p>

            <p>This link expires in 1 hour.</p>

            <p>If you did not request this, please ignore this email.</p>
        """
    }

    response = requests.post(
        url,
        json=data,
        headers=headers
    )

    print("🔥 PASSWORD RESET STATUS:", response.status_code)
    print("🔥 PASSWORD RESET RESPONSE:", response.text)

    return response.status_code




import requests
from django.conf import settings





def send_password_changed_email(user):
    print("🔥 PASSWORD EMAIL FUNCTION CALLED")

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "api-key": settings.BREVO_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "sender": {
            "name": "SJS Company Security",
            "email": "smangajsithole@gmail.com"
        },
        "to": [{"email": user.email}],
        "subject": "Password Changed Successfully",
        "htmlContent": f"""
            <h2>Hello {user.first_name}</h2>
            <p>Your password has been changed successfully.</p>
            <p>If this was you, ignore this email.</p>
        """
    }

    response = requests.post(url, json=data, headers=headers)

    print("🔥 STATUS:", response.status_code)
    print("🔥 RESPONSE:", response.text)

    return response.status_code



def send_new_signup_admin_email(user):
    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "api-key": settings.BREVO_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "sender": {
            "name": "SJS Company Notifications",
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "to": [
            {
                "email": settings.ADMIN_NOTIFICATION_EMAIL
            }
        ],
        "subject": "New User Registration",
        "htmlContent": f"""
            <h2>New User Registration</h2>

            <p>A new user has verified their email address and activated their account.</p>

            <p>{user.first_name}</p>
        """
    }

    response = requests.post(
        url,
        json=data,
        headers=headers
    )

    if response.status_code != 201:
        raise Exception(
            f"BREVO ERROR {response.status_code}: {response.text}"
        )

    return response.status_code
