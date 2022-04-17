
from django.urls import path,include, re_path
from accounts.views import AccountProfileModelTemplateView,AccountProfileModelDetailView, AccountProfileModelListView, AccountProfileModelUpdateView, AccountProfileModelDeleteView, AccountProfileModelCreateView

urlpatterns = [    
    path("", AccountProfileModelTemplateView.as_view(), name="accountprofilemodel-index"),    
    path("collection/", AccountProfileModelListView.as_view(), name="accountprofilemodel-list"),
    path("collection/<int:pk>/", AccountProfileModelDetailView.as_view(), name='accountprofilemodel-detail'),
    path("collection/<int:pk>/editar/", AccountProfileModelUpdateView.as_view(), name='accountprofilemodel-update'),
    path("collection/<int:pk>/remover/", AccountProfileModelDeleteView.as_view(), name='accountprofilemodel-delete'),    
    path("collection/adicionar/", AccountProfileModelCreateView.as_view(), name='accountprofilemodel-create'),
]