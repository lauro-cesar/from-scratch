
from django.urls import path,include, re_path
from accounts.views import AccountProfileModelTemplateView,AccountProfileModelDetailView, AccountProfileModelListView, AccountProfileModelUpdateView, AccountProfileModelDeleteView, AccountProfileModelCreateView

urlpatterns = [    
    path("", AccountProfileModelTemplateView.as_view(template_name="accountprofilemodel/app_templates/accountprofilemodel_index.html"), name="accountprofilemodel-index"),    
    path("collection/", AccountProfileModelListView.as_view(template_name = "accountprofilemodel/app_templates/accountprofilemodel_list.html"), name="accountprofilemodel-list"),
    path("collection/<int:pk>/", AccountProfileModelDetailView.as_view(template_name = "accountprofilemodel/app_templates/accountprofilemodel_detail.html"), name='accountprofilemodel-detail'),
    path("collection/<int:pk>/editar/", AccountProfileModelUpdateView.as_view(template_name = "accountprofilemodel/app_templates/accountprofilemodel_update.html"), name='accountprofilemodel-update'),
    path("collection/<int:pk>/remover/", AccountProfileModelDeleteView.as_view(template_name = "accountprofilemodel/app_templates/accountprofilemodel_delete.html"), name='accountprofilemodel-delete'),    
    path("collection/adicionar/", AccountProfileModelCreateView.as_view(template_name = "accountprofilemodel/app_templates/accountprofilemodel_create.html"), name='accountprofilemodel-create'),
]