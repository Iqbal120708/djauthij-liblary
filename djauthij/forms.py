from django import forms
from django.contrib.auth import get_user_model

class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Password Confirm",
        widget=forms.PasswordInput
    )
    
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]
        
        
    def clean(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        
        if p1 != p2:
            raise forms.ValidationError("Password tidak sama")
            
    def save(self):
        user = super().save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user
            
        