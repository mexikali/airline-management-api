from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def not_found(request, exception):
    response_data = {
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist. Please check the URL.",
        "status": 404
    }
    return JsonResponse(response_data, status=404)


def send_email(subject, message, recipient_list, content_type='html'):
    try:
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        email.content_subtype = content_type
        email.send()
        logger.info(f"Email sent successfully: {recipient_list}")
    except Exception as e:
        logger.error(f"Email could not be sent: {recipient_list}\nerror: {e}")