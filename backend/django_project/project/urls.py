from django.contrib import admin
from django.urls import path, include, converters
from django.conf import settings
from .views import CustomAuthToken
from project.admin import ProjectAdminSite, project_dashboard_site, project_admin_site

urlpatterns = [    
    path("admin/", admin.site.urls),
    path("dashboard/", 
            include(
            [             
                path("", project_dashboard_site.urls)                
            ]
        ),    
    ), 

    path(r"api-token-auth/", CustomAuthToken.as_view(), name="get-token-auth"),        
    path(
        "accounts/",
        include(
            [
                path("", include("accounts.urls")),
                path("", include("django.contrib.auth.urls")),
            ]
        ),
    ),
    path("app/", include([
        path("v1/",include([
            path("profile/", include("accounts.app_routes.v1.accounts"))
        ])),
        ])),      
    path(
        "rest-api/v1/app/",
        include(
            [
                path("", include("accounts.rest_urls")),
         
                  
            ]
        ),
    ),
    path(
        "rest-api/v1/",
        include(
            [
                path("", include("accounts.rest_urls")),                                    
            ]
        ),
    ),

    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("django.contrib.flatpages.urls")),
]
