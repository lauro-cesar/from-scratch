
import logging
logger = logging.getLogger(__name__)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
from django.conf import settings
import base64
from django.urls import reverse
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
from project.models import BaseModel, StackedModel



class AccountProfileModel(BaseModel):
    SERIALIZABLES =['id','label']
    READ_ONLY_FIELDS=[]
    ADMIN_LIST_EDITABLE=[]
    ADMIN_LIST_DISPLAY=['label']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=[]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=['label']
    EXCLUDE_FROM_ADMIN=[]
    CREATE_FIELDS=[]
    FORM_FIELDS=[]
 
    TASKS={
        'on_create':["accounts_collection_accountprofilemodel"],
        'on_save':["stream_live_update_accountprofilemodel"],
        'on_delete':[]
    }

    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL,related_name="accountprofilemodel_criados_por_mim")

    modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True ,blank=True, on_delete=models.SET_NULL,related_name="accountprofilemodel_modificados_por_mim")

    removido_por = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL,related_name="accountprofilemodel_removidos_por_mim")

    def get_list_url(self):
        return reverse('accountprofilemodel-list')

    def get_absolute_url(self):
        return reverse('accountprofilemodel-detail', args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse('accountprofilemodel-delete', args=[str(self.id)])

    def get_detail_url(self):
        return reverse('accountprofilemodel-detail', args=[str(self.id)])
    
    def get_create_url(self):
        return reverse('accountprofilemodel-create')

    def get_update_url(self):
        return reverse('accountprofilemodel-update', args=[str(self.id)])

    cpf = models.CharField(max_length=256,blank=True,null=True,unique=True)


    @property
    def label(self):
        return self.cpf


    class Meta(BaseModel.Meta):
        verbose_name = _("Perfil")
        verbose_name_plural = _("Perfis")

    def __str__(self):
        return self.label
