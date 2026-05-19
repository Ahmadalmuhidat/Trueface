from django.conf import settings
from django.core.mail import EmailMessage


def SendEmailTemplate(subject: str, html_content: str, recipient_list: list[str]) -> bool:
  try:
    email = EmailMessage(subject=subject, body=html_content, from_email=settings.EMAIL_HOST_USER, to=recipient_list)
    email.content_subtype = "html"
    email.send(fail_silently=False)
    return True
  except Exception as e:
    print(f"Error sending HTML email: {e}")
    return False
