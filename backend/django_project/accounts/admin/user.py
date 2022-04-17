"""[summary]

[description]

Variables:
    User {[type]} -- [description]
"""
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from project.celery_tasks import app
from django.contrib import messages
User = get_user_model()
from django.utils.safestring import mark_safe
from project.admin import dashboard_sites

@admin.register(User)
class UserAdmin(UserAdmin):    
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        campos = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            return ((None, {'fields': ('username', 'password')}),(_('Personal info'), {'fields': ('first_name', 'last_name', 'email','avatar')}),(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_appuser','groups', 'user_permissions'),}),(_('Important dates'), {'fields': ('last_login', 'date_joined')}),)          

        return ((None, {'fields': ('username', 'password')}),(_('Personal info'), {'fields': ('first_name', 'last_name', 'email','avatar')}),)          

    def get_form(self, request, obj=None, **kwargs):   
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form    
        form = super().get_form(request, obj, **defaults)        
        return form


    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()
        if not request.user.is_superuser:
            qs = qs.filter(pk=request.user.id)

        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    save_on_top = True
 #   list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    list_display = ["username", "avatar_url", "first_name", "last_name", "email"]
    
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    # form = UserChangeForm
    # add_form = UserCreationForm
    # change_password_form = AdminPasswordChangeForm

    def avatar_url(self, obj):  # receives the instance as an argument
    
        return mark_safe(
            '<img width=96px src="{url}" />'.format(
                url=obj.get_avatar_url,
            )
        )
    
    avatar_url.allow_tags = True
    avatar_url.short_description = "Avatar"

    def has_delete_permission(self, request, obj=None):
        return False


for admin_site in dashboard_sites:
    admin_site.register(User,UserAdmin)