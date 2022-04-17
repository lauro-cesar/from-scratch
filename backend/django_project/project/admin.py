from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext as _, gettext_lazy

class BaseModelAdmin(admin.ModelAdmin):
    admin_priority = 20
    default_lon = -5372220.98 
    default_lat = -2413950.78
    map_width = 800
    map_height = 600
    default_zoom = 8
    save_on_top = True
    date_hierarchy = "created"
    list_per_page = 15
    list_max_show_all = 50
    actions_on_bottom = True
    EXCLUDE_FROM_ADMIN = []    
    exclude = [
         "criado_por","modificado_por","removido_por","isRemoved",
        "isActive", "isDone", "isComplete", "isPublic", "isProcessed","alterado_por"]


class BaseModelAdminTabular(admin.TabularInline):
    ""


class ProjectAdminSite(admin.AdminSite):
    site_header = _("Api gateway")
    site_title = _("Admin Dashboard")
    index_title = _('Api Gateway') 
    enable_nav_sidebar = True
    

    def each_context(self, request):        
        self.request= request
        contexto = super().each_context(request)
        contexto.update({
            "rest_api_address":f"{settings.REST_API_ADDRESS}",
            "socket_api_address":f"{settings.SOCKET_API_ADDRESS}",   
        })
        return contexto

project_admin_site = ProjectAdminSite(name="admin_api")


class ProjectDashboardSite(admin.AdminSite):
    site_header = _("Admin Dashboard")
    site_title = _("Admin Dashboard")
    index_title = _('Dashboard') 
    enable_nav_sidebar = True
    

    def each_context(self, request):        
        self.request= request
        contexto = super().each_context(request)
        contexto.update({
            "rest_api_address":f"{settings.REST_API_ADDRESS}",
            "socket_api_address":f"{settings.SOCKET_API_ADDRESS}",   
        })
        return contexto

project_dashboard_site = ProjectDashboardSite(name="dashboard")

admin_sites = [project_admin_site]
dashboard_sites =[project_dashboard_site]