from django.test import TestCase
from djauthij.models import OTPVerifications
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from django.urls import reverse
from freezegun import freeze_time
from unittest.mock import patch

@freeze_time("2026-02-24 10:00:00")
class TestVerifyOTP(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="secret123",
            is_active=False
        )
        
        created_at = now()
        expired_at = created_at + timedelta(minutes=5)
    
        cls.otp =  OTPVerifications.objects.create(
            user=cls.user,
            otp="123456",
            created_at=created_at,
            expired_at=expired_at,
        )
        
    def test_otp_invalid(self):
        res = self.client.post(reverse("verify_otp"), data={
            "otp_code": "abcdef"
        })
        
        self.assertContains(res, "Hanya boleh angka positif.")
        
    @freeze_time("2026-02-24 11:00:00")
    def test_otp_expired(self):
        session = self.client.session
        session["pending_user_email"] = self.user.email
        session.save()
        
        res = self.client.post(reverse("verify_otp"), data={
            "otp_code": "123456"
        })
        
        self.assertContains(res, "Kode OTP tidak valid atau sudah kadaluwarsa.")
        
    @patch("djauthij.views.UserModel.save")
    def test_error_transaction_db(self, mock_save):
        mock_save.side_effect = Exception("DB error")
        
        session = self.client.session
        session["pending_user_email"] = self.user.email
        session.save()
        
        res = self.client.post(reverse("verify_otp"), data={
            "otp_code": "123456"
        })
        
        self.assertRedirects(res, reverse("verify_otp"))
        
        # pastikan ke rollback
        self.otp.refresh_from_db()
        self.assertFalse(self.otp.is_used)
        
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        
    def test_success(self):
        session = self.client.session
        session["pending_user_email"] = self.user.email
        session.save()
        
        res = self.client.post(reverse("verify_otp"), data={
            "otp_code": "123456"
        })
        
        self.assertRedirects(res, reverse("login"))
        
        self.otp.refresh_from_db()
        self.assertTrue(self.otp.is_used)
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)