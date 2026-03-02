from django.contrib import admin
from .models import CustomUser, OTPVerifications

# Register your models here.
class SuperuserOnlyAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.action(description="Soft delete (nonaktifkan user)")
def soft_delete_users(modeladmin, request, queryset):
    for user in queryset:
        user.soft_delete()
        
@admin.action(description="Hard delete (PERMANEN)")
def hard_delete_users(modeladmin, request, queryset):
    if not request.user.is_superuser:
        modeladmin.message_user(
            request,
            "Hanya superuser yang boleh hard delete",
            level=messages.ERROR,
        )
        return

    for user in queryset:
        user.hard_delete()
        
@admin.register(CustomUser)
class CustomUserAdmin(SuperuserOnlyAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
        
admin.site.register(OTPVerifications, SuperuserOnlyAdmin)