from django.test import TestCase
from django.contrib.messages import get_messages
from django.urls import reverse
from djauthij.models import OTPVerifications
from unittest.mock import patch
from django.contrib.auth import get_user_model

class TestRegister(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="secret123"
        )
        
        cls.form_data = {
            "username": "test",
            "email": "test@gmail.com",
            "password1": "secret123",
            "password2": "secret123",
        }
        
    def test_user_already_registered(self):
        response = self.client.post(reverse("register"), data=self.form_data)
    
        self.assertRedirects(response, reverse("login"))
    
        messages = list(get_messages(response.wsgi_request))
    
        self.assertTrue(len(messages) > 0)
    
        self.assertEqual(str(messages[0]), "Email ini sudah terdaftar, Silakan login")
    
    @patch("djauthij.views.send_otp_email")
    def test_user_exists_and_not_active(self, mock_send_email):
        self.user.is_active = False
        self.user.save()
        
        response = self.client.post(reverse("register"), data=self.form_data)
        
        self.assertRedirects(response, reverse("verify_otp"))
        
        self.assertEqual(OTPVerifications.objects.count(), 1)
        
        instance_otp = OTPVerifications.objects.filter(user=self.user).first()
        self.assertTrue(instance_otp)
        
        self.assertEqual(self.client.session["pending_user_email"], self.user.email)
        
        mock_send_email.assert_called_once_with(
            self.user.email,
            instance_otp.otp
        )
    
    @patch("djauthij.views.send_otp_email")
    def test_success(self, mock_send_email):
        self.form_data["username"] = "test2"
        self.form_data["email"] = "test2@gmail.com"
        
        response = self.client.post(reverse("register"), data=self.form_data)
        
        self.assertEqual(get_user_model().objects.count(), 2)
        
        self.assertRedirects(response, reverse("verify_otp"))
        
        self.assertEqual(OTPVerifications.objects.count(), 1)
        
        instance_otp = OTPVerifications.objects.filter(user__email="test2@gmail.com").first()
        self.assertTrue(instance_otp)
        
        self.assertEqual(self.client.session["pending_user_email"], "test2@gmail.com")
        
        mock_send_email.assert_called_once_with(
            "test2@gmail.com",
            instance_otp.otp
        )