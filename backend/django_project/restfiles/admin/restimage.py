
from django.contrib import admin
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
import base64
from django.utils.translation import gettext_lazy as _
from project.admin import BaseModelAdmin
from restfiles.models import RestImageModel


@admin.register(RestImageModel)
class RestImageModelAdmin(BaseModelAdmin):
    save_on_top = True
    ordering = RestImageModel.ADMIN_ORDERING
    list_display = RestImageModel.ADMIN_LIST_DISPLAY+['img_url','rest_data']
    list_filter = RestImageModel.ADMIN_LIST_FILTER
    search_fields = RestImageModel.ADMIN_SEARCH_FILTER
    list_editable = RestImageModel.ADMIN_LIST_EDITABLE
    list_display_links=RestImageModel.ADMIN_DISPLAY_LINKS
    actions=['generate_rest_image_raw_data']

    def generate_rest_image_raw_data(self, request, queryset):
        for obj in queryset:
            try:
                result = app.send_task("generate_rest_image_raw_data", [obj.id])
            except Exception as e:
                self.message_user(
                    request,
                    "{label}: Erro ao enviar para a fila de processamento".format(
                        label=obj
                    ),
                    messages.ERROR,
                )
            else:
                self.message_user(
                    request,
                    "{label}: enviado para a fila de processamento".format(label=obj),
                    messages.SUCCESS,
                )

    generate_rest_image_raw_data.short_description = _("Gerar rest data")
    generate_rest_image_raw_data.allowed_permissions = ['generate_rest_image_raw_data']

    def has_generate_rest_image_raw_data_permission(self,request, obj=None):
        return request.user.is_superuser   

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):	        
        return True

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def img_url(self, obj):  # receives the instance as an argument
        return mark_safe(
            '<img width=96px src="{url}" />'.format(
                url=obj.original.url,
            )
        )
    img_url.allow_tags = True
    img_url.short_description = "Original"

    def rest_data(self, obj):  # receives the instance as an argument
        return mark_safe(
            f"""<img width=96px src="data:image/png;base64, {obj.raw_data}" />"""
        )
        
    rest_data.allow_tags = True
    rest_data.short_description = "Rest data"
