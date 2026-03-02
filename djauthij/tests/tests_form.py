from django.test import TestCase
from django.contrib.auth import get_user_model
from djauthij.forms import CreateUserForm

class TestForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data = {
            "username": "test",
            "email": "test@gmail.com",
            "password1": "secret123",
            "password2": "secret123",
        }
        
    def test_success(self):
        form = CreateUserForm(data=self.form_data)

        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, "test")
        self.assertFalse(user.is_active)
    
    def test_password_invalid(self):
        self.form_data["password2"] = "secret999"
        form = CreateUserForm(data=self.form_data)

        self.assertFalse(form.is_valid())

        errors = form.non_field_errors()
        self.assertIn("Password tidak sama", errors)