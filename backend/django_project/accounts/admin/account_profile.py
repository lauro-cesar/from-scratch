
from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import BaseModelAdmin
from accounts.models import AccountProfileModel


@admin.register(AccountProfileModel)
class AccountProfileModelAdmin(BaseModelAdmin):
    save_on_top = True
    ordering = AccountProfileModel.ADMIN_ORDERING
    list_display = AccountProfileModel.ADMIN_LIST_DISPLAY
    list_filter = AccountProfileModel.ADMIN_LIST_FILTER
    search_fields = AccountProfileModel.ADMIN_SEARCH_FILTER
    list_editable = AccountProfileModel.ADMIN_LIST_EDITABLE
    list_display_links=AccountProfileModel.ADMIN_DISPLAY_LINKS
    filter_horizontal= AccountProfileModel.ADMIN_FILTER_HORIZONTAL
    exclude = BaseModelAdmin.exclude + AccountProfileModel.EXCLUDE_FROM_ADMIN
    actions=['stream_live_update_accountprofilemodel']

    def stream_live_update_accountprofilemodel(self, request, queryset):
        for obj in queryset:
            try:
                result =  app.send_task("stream_live_update_accountprofilemodel",[obj.id])
            except Exception as e:
                self.message_user(
                    request,
                    f"{obj.label}: {e.__repr__()}",
                    messages.ERROR,
                )
            else:
                self.message_user(
                    request,
                    "{label}: enviado para a fila de processamento".format(label=obj),
                    messages.SUCCESS,
                )

    stream_live_update_accountprofilemodel.short_description = _("Send to stream")
    stream_live_update_accountprofilemodel.allowed_permissions = ['stream_live_update_accountprofilemodel']

    def has_stream_live_update_accountprofilemodel_permission(self,request, obj=None):
        return request.user.is_superuser  



    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):	        
        return True

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
