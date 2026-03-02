from django.shortcuts import render, redirect
from .forms import CreateUserForm
from .tasks import send_otp_email
from .utils import generate_otp
from django.contrib.auth import get_user_model
from .models import OTPVerifications
from django.db import transaction
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

UserModel = get_user_model()

# Create your views here.
def register(request):
    if request.POST:
        form = CreateUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = UserModel.objects.filter(email=email).first()
            if user and user.is_active:
                messages.info(request, "Email ini sudah terdaftar, Silakan login")
                return redirect("login")
                
            # jika user belum ada buat data dulu
            if not user:
                user = form.save()
            
            otp_code = generate_otp(user)
            request.session['pending_user_email'] = user.email
            send_otp_email(user.email, otp_code)
            return redirect("verify_otp")
    else:
        form = CreateUserForm()
    return render(request, "registration/register.html", {"form":form})
    
def verify_otp(request):
    if request.POST:
        otp_code = request.POST.get("otp_code")
        if not otp_code.isdigit():
            return render(request, 'registration/otp_form.html', {
                'error_otp': "Hanya boleh angka positif."
            })
        
        email = request.session['pending_user_email']
        latest_otp = OTPVerifications.objects.filter(
            user__email=email, 
            otp=otp_code, 
            is_used=False,
        ).order_by('-created_at').first()
        
        if latest_otp and latest_otp.created_at <= now() <= latest_otp.expired_at:
            try: 
                with transaction.atomic():
                    latest_otp.is_used = True
                    latest_otp.save()
                    
                    user = latest_otp.user
                    user.is_active = True
                    user.save()
                    
                    messages.success(request, "Akun berhasil diaktivasi! Silakan login.")
                    return redirect("login")
            except Exception as e:
                messages.error(request, "Terjadi kesalahan saat aktivasi. Silakan coba lagi.")
                return redirect("verify_otp")
        else:
            return render(request, 'registration/otp_form.html', {
                'error_otp': "Kode OTP tidak valid atau sudah kadaluwarsa."
            })
            
    return render(request, 'registration/otp_form.html')
   
@login_required 
def profile(request):
    return render(request, "registration/profile.html")