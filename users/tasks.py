from django.core.mail import send_mail

from car_dealership.celery import app as celery_app
from users.models import UserProfile
from users.services import (
    email_context_account_confirmation,
    email_context_change_email,
    email_context_change_login,
    email_context_reset_password,
)


@celery_app.task
def email_account_confirmation(user_pk: int):
    """
    Function to send email with link to confirm registration.

    Parameters
    ----------
    user_pk: int
        PrimaryKey of UserProfile
    """
    user = UserProfile.objects.filter(pk=user_pk).first()

    if user:
        (
            subject,
            alternative_text,
            from_email,
            recipient_list,
            html_message,
        ) = email_context_account_confirmation(user)

        send_mail(
            subject,
            alternative_text,
            from_email,
            recipient_list,
            html_message=html_message,
        )


@celery_app.task
def email_reset_password(user_pk: int):
    """
    Function to send email with link to reset password.

    Parameters
    ----------
    user_pk: int
        PrimaryKey of UserProfile
    """
    user = UserProfile.objects.filter(pk=user_pk).first()
    if user:
        (
            subject,
            alternative_text,
            from_email,
            recipient_list,
            html_message,
        ) = email_context_reset_password(user)

        send_mail(
            subject,
            alternative_text,
            from_email,
            recipient_list,
            html_message=html_message,
        )


@celery_app.task
def email_change_email(user_pk: int):
    """
    Function to send email with link to change email.

    Parameters
    ----------
    user_pk: int
        PrimaryKey of UserProfile
    """
    user = UserProfile.objects.filter(pk=user_pk).first()
    if user:
        (
            subject,
            alternative_text,
            from_email,
            recipient_list,
            html_message,
        ) = email_context_change_email(user)

        send_mail(
            subject,
            alternative_text,
            from_email,
            recipient_list,
            html_message=html_message,
        )


@celery_app.task
def email_change_login(user_pk: int):
    """
    Function to send email with link to change login.

    Parameters
    ----------
    user_pk: int
        PrimaryKey of UserProfile
    """
    user = UserProfile.objects.filter(pk=user_pk).first()
    if user:
        (
            subject,
            alternative_text,
            from_email,
            recipient_list,
            html_message,
        ) = email_context_change_login(user)

        send_mail(
            subject,
            alternative_text,
            from_email,
            recipient_list,
            html_message=html_message,
        )
