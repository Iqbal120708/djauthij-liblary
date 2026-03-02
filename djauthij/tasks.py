from huey.contrib.djhuey import task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .conf import APP_NAME, EMAIL_HOST_USER

@task(retries=3, retry_delay=60)
def send_otp_email(user_email, otp_code):
    subject = 'Kode Verifikasi Akun'
    from_email = f"{APP_NAME} <{EMAIL_HOST_USER}>"
    to = [user_email]

    html_content = render_to_string('registration/otp_email.html', {'otp': otp_code})
    
    text_content = strip_tags(html_content) 

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
