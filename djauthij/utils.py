import secrets
import string
from .models import OTPVerifications
from django.utils.timezone import now
from datetime import timedelta

def generate_otp(user, length=6):
    characters = string.digits
    otp = ''.join(secrets.choice(characters) for _ in range(length))
    
    # OTPVerifications.objects.filter(user=user, is_used=False).update(is_used=True)
    
    created_at = now()
    expired_at = created_at + timedelta(minutes=5)
    OTPVerifications.objects.create(
        user=user,
        otp=otp,
        created_at=created_at,
        expired_at=expired_at,
    )
    
    return otp

