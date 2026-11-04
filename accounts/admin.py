from functools import wraps

from django.contrib import admin
from django.http import HttpResponseForbidden
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


class CampusAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return (
            super().has_permission(request)
            and request.user.role == CustomUser.Role.ADMIN
        )

    def admin_view(self, view, cacheable=False):
        admin_view = super().admin_view(view, cacheable)

        @wraps(view)
        def role_protected_view(request, *args, **kwargs):
            if request.user.is_authenticated and not self.has_permission(request):
                return HttpResponseForbidden("You do not have permission to access this page.")
            return admin_view(request, *args, **kwargs)

        return role_protected_view

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    def login(self, request, extra_context=None):
        if request.user.is_authenticated and not self.has_permission(request):
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().login(request, extra_context)


campus_admin_site = CampusAdminSite(name="admin")

# Register your models here.
@admin.register(CustomUser, site=campus_admin_site)
class CustomAdmin(UserAdmin):
    list_display = ['last_name', 'first_name','username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ("School Profile", {'fields': ('role', 'course')}),
    )

