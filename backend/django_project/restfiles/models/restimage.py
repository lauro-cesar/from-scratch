
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
from django.conf import Settings, settings
import base64
from django.core.cache import cache
from django.utils.safestring import mark_safe
from project.celery_tasks import app
from django.contrib import messages
from project.models import BaseModel, StackedModel
from PIL import Image, ImageOps, ImageDraw,ImageFont
from io import BytesIO
import base64


class RestImageModel(BaseModel):
    SERIALIZABLES =['id','imagem_raw_data']
    READ_ONLY_FIELDS=[]
    ADMIN_LIST_EDITABLE=['altura','largura','raw_data_ready']
    ADMIN_LIST_DISPLAY=['label','altura','largura','raw_data_ready']
    ADMIN_ORDERING=[]
    ADMIN_FILTER_HORIZONTAL= []
    ADMIN_LIST_FILTER=[]
    ADMIN_SEARCH_FILTER=[]
    ADMIN_DISPLAY_LINKS=['label']

    TASKS={
        'on_create':[],
        'on_save':['generate_rest_image_raw_data'],
        'on_delete':[]
    }
    nome =models.CharField(max_length=128,verbose_name=_("Referencia"))
    largura = models.PositiveSmallIntegerField(default=128)
    altura = models.PositiveSmallIntegerField(default=128)    
    original = models.ImageField(upload_to="restimages/originals/",verbose_name=_("Original"))  
    imagem_raw_data = models.TextField(blank=True)
    raw_data_ready = models.BooleanField(default=False)

    @property
    def default_raw_data(self):
        im = Image.open(f"{settings.BASE_DIR}/static/icons/default.png")
        im.thumbnail((self.largura,self.altura), Image.ANTIALIAS)
        buffered = BytesIO()
        im.save(buffered, format="PNG")
        raw_data = smart_str(base64.b64encode(buffered.getvalue()))
        im.close()
        return raw_data

    @property
    def raw_data(self):
        if self.raw_data_ready:
            return self.imagem_raw_data
        return self.default_raw_data


    @property
    def label(self):
        return self.nome

    class Meta(BaseModel.Meta):
        verbose_name = _("Rest image")
        verbose_name_plural = _("Rest image")


    def __str__(self):
        return self.label
