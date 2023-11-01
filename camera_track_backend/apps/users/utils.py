from django.core.mail import send_mail

from camera_track.settings.base import EMAIL_HOST_USER


def email_notification(sjt: str, msg: str, address: list, sender=EMAIL_HOST_USER, failure=False):
    send_mail(
        subject=sjt,
        message=msg,
        from_email=sender,
        recipient_list=address,
        fail_silently=failure
    )
