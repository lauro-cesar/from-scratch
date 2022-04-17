from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import json
from functools import reduce
from django.utils.functional import cached_property
import hashlib
from django.conf import settings


class User(AbstractUser):
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
        'on_create':['create_auth_token'],
        'on_save':[],
        'on_delete':[]
    }

    dateCreated = models.DateTimeField(auto_now=True)
    lastModified = models.DateTimeField(auto_now=True)
    testUser = models.BooleanField(default=False)
    guestUser = models.BooleanField(default=False)
    validEmail = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatares/",blank=True, null=True, verbose_name=_("Foto do usuario") )
    is_appuser=models.BooleanField(default=False,verbose_name=_("Pode acessar o app"))
    
    @property
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return "/static/icons/user.png"
        
            
    @property
    def fullName(self):
        return self.get_full_name()


    @property
    def label(self):
        return self.fullName

    def syncAccount(self):
        pass 
    
    def getSSOToken(self):
        token = default_token_generator.make_token(self)
        uidb64 = urlsafe_base64_encode(str(self.pk).encode())
        return {"token": token, "uidb64": uidb64}    


    def getSessionToken(self):
        token = default_token_generator.make_token(self)
        uidb64 = urlsafe_base64_encode(str(self.pk).encode())
        return {"token": token, "uidb64": uidb64}


    @property
    def servidores(self):
        return []

    @property
    def app_settings(self):
        return {}

    @property
    def authToken(self):
        token = None
        try:
            token = Token.objects.get(user=self)
        except Exception:
            pass

        if not token:
            token = Token.objects.create(user=self)
        return token.key
    
    @property
    def token(self):
        return self.authToken

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def __str__(self):
        return self.fullName
