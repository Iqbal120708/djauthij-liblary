from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
class TestProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="test",
            email="test@gmail.com",
            password="secret123"
        )
        
    def test_success(self):
        self.client.force_login(self.user)
        
        res = self.client.post(reverse("profile"))
        
        self.assertEqual(res.status_code, 200)
        
    def test_not_logged_in(self):
        res = self.client.post(reverse("profile"))
        
        self.assertRedirects(
            res,
            reverse("login") + "?next=" + reverse("profile")
        )
        self.assertEqual(res.status_code, 302)
        