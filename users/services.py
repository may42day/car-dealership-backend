from django.conf import settings
from django.template.loader import render_to_string

from users.models import ConfirmationToken, UserProfile


def generate_message_data(
    user: UserProfile, subject: str, template_name: str, link: str = None
) -> (str, list, str):
    """
    Function to generate date for email message.
    Generates common data for all emails. Renders html templates into string.

    Parameters
    ----------
    user: UserProfile
        UserProfile instance for whom email sents
    subject: str
        subject of email letter
    template_name: str
        template path for email letter
    link: int
        link with token for email

    Returns
    ----------
    from_email: str
        email address of sender
    recipient_list: list
        emails' address list
    html_message: str
        generated email template into string

    """
    from_email = settings.EMAIL_HOST_USER
    context = {
        "subject": subject,
    }
    if link:
        context.update({"link": link})

    html_message = render_to_string(template_name, context)
    recipient_list = [user.email]
    return from_email, recipient_list, html_message


def email_context_account_confirmation(user: UserProfile) -> (str, str, str, list, str):
    """
    Function to generate date for email message with register confirmation.

    Parameters
    ----------
    user: UserProfile
        UserProfile instance for whom email sents.

    Returns
    ----------
    subject: str
        subject of email letter.
    alternative_text: str
        message text for cases when service can't handle html.
    from_email: str
        email address of sender.
    recipient_list: list
        emails' address list.
    html_message: str
        generated email template into string.
    """
    subject = "[CarDealership] Please confirm your registration"
    template_name = "users/confirm_registration.html"
    token = ConfirmationToken.objects.create(
        user=user, token_type=ConfirmationToken.REG_CONFIRM
    )
    link = token.create_link()

    alternative_text = (
        f"Hello, {user.username}!\nFollow the link to confirm your registration. {link}"
    )
    (
        from_email,
        recipient_list,
        html_message,
    ) = generate_message_data(user, subject, template_name, link)
    return subject, alternative_text, from_email, recipient_list, html_message


def email_context_change_email(user: UserProfile) -> (str, str, str, list, str):
    """
    Function to generate date for email message to change email.

    Parameters
    ----------
    user: UserProfile
        UserProfile instance for whom email sents.

    Returns
    ----------
    subject: str
        subject of email letter.
    alternative_text: str
        message text for cases when service can't handle html.
    from_email: str
        email address of sender.
    recipient_list: list
        emails' address list.
    html_message: str
        generated email template into string.
    """
    subject = "[CarDealership] Instructions to change email"
    template_name = "users/change_email.html"
    token = ConfirmationToken.objects.create(
        user=user, token_type=ConfirmationToken.EMAIL_CHANGE
    )
    link = token.create_link()
    alternative_text = f"Hello, {user.username}!"
    (
        from_email,
        recipient_list,
        html_message,
    ) = generate_message_data(user, subject, template_name, link)
    return subject, alternative_text, from_email, recipient_list, html_message


def email_context_change_login(user: UserProfile) -> (str, str, str, list, str):
    """
    Function to generate date for email message to change login.

    Parameters
    ----------
    user: UserProfile
        UserProfile instance for whom email sents.

    Returns
    ----------
    subject: str
        subject of email letter.
    alternative_text: str
        message text for cases when service can't handle html.
    from_email: str
        email address of sender.
    recipient_list: list
        emails' address list.
    html_message: str
        generated email template into string.
    """
    subject = "[CarDealership] Instructions to change login"
    template_name = "users/change_login.html"
    token = ConfirmationToken.objects.create(
        user=user, token_type=ConfirmationToken.LOGIN_CHANGE
    )
    link = token.create_link()
    alternative_text = f"Hello, {user.username}!"
    (
        from_email,
        recipient_list,
        html_message,
    ) = generate_message_data(user, subject, template_name, link)
    return subject, alternative_text, from_email, recipient_list, html_message


def email_context_reset_password(user: UserProfile) -> (str, str, str, list, str):
    """
    Function to generate date for email message to reset password.

    Parameters
    ----------
    user: UserProfile
        UserProfile instance for whom email sents.

    Returns
    ----------
    subject: str
        subject of email letter.
    alternative_text: str
        message text for cases when service can't handle html.
    from_email: str
        email address of sender.
    recipient_list: list
        emails' address list.
    html_message: str
        generated email template into string.
    """
    subject = "[CarDealership] Instructions to reset password"
    template_name = "users/reset_password.html"
    token = ConfirmationToken.objects.create(
        user=user, token_type=ConfirmationToken.PASSW_RESET
    )
    link = token.create_link()

    alternative_text = (
        f"Hello, {user.username}!\nFollow the link to reset password {link}"
    )
    (
        from_email,
        recipient_list,
        html_message,
    ) = generate_message_data(user, subject, template_name, link)
    return subject, alternative_text, from_email, recipient_list, html_message
