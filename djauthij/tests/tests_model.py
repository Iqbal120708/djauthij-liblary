from django.test import TestCase
from django.contrib.auth import get_user_model
from djauthij.models import OTPVerifications
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str

class TestModelCustomUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="secret123"
        )
        
    def test_delete(self):
        with self.assertRaises(RuntimeError) as e:
            self.user.delete()
    
        error = e.exception
        self.assertEqual(str(error), "Gunakan soft_delete() atau hard_delete()")
        
    def test_soft_delete(self):
        # pastikan True
        self.assertTrue(self.user.is_active)
        
        self.user.soft_delete()
        
        self.user.refresh_from_db()
        
        # pastikan False setelah soft delete
        self.assertFalse(self.user.is_active)
        
    def test_hard_delete(self):
        self.user.hard_delete()
        
        User = get_user_model()
        user = User.objects.filter(email="test@gmail.com")
    
        self.assertFalse(user.exists())
        

class TestModelOTPVerifications(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="secret123"
        )
        
    def test_otp_invalid(self):
        otp = "abcdef"
        
        created_at = now()
        expired_at = created_at + timedelta(minutes=5)
    
        with self.assertRaises(ValidationError) as e:
            OTPVerifications.objects.create(
                user=self.user,
                otp=otp,
                created_at=created_at,
                expired_at=expired_at,
            )
            
        error = e.exception

        msg = force_str(error.messages[0])
        self.assertEqual(msg, "Kode OTP harus berupa angka.")
        
    def test_invalid_expire_date(self):
        otp = "123456"
        
        created_at = now()
        expired_at = created_at - timedelta(minutes=1)
    
        with self.assertRaises(ValidationError) as e:
            OTPVerifications.objects.create(
                user=self.user,
                otp=otp,
                created_at=created_at,
                expired_at=expired_at,
            )
            
        error = e.exception

        msg = force_str(error.messages[0])
        self.assertEqual(msg, "Waktu kedaluwarsa tidak boleh lebih awal dari waktu pembuatan.")
            
    def test_success(self):
        otp = "123456"
        
        created_at = now()
        expired_at = created_at + timedelta(minutes=5)
    
        OTPVerifications.objects.create(
            user=self.user,
            otp=otp,
            created_at=created_at,
            expired_at=expired_at,
        )
        
        self.assertEqual(OTPVerifications.objects.count(), 1)