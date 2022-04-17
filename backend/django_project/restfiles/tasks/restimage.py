
from celery import shared_task
from django.conf import settings
from django.utils.encoding import smart_str
from PIL import Image, ImageOps, ImageDraw,ImageFont
from io import BytesIO
import base64

from django.core.cache import cache
from django.utils.text import slugify
import json
from django.urls import reverse_lazy

from project.celery_tasks import app
from restfiles.models import RestImageModel


@shared_task(name="generate_rest_image_raw_data", max_retries=2, soft_time_limit=45)
def on_generate_rest_image_raw_data_task(ID):  
    instance = RestImageModel.get_or_none(pk=ID,raw_data_ready=False)
    if instance:
        print("gerar rest")
        im = Image.open(instance.original)
        im.thumbnail((instance.largura,instance.altura), Image.ANTIALIAS)
        buffered = BytesIO()
        im.save(buffered, format="PNG")
        instance.imagem_raw_data = smart_str(base64.b64encode(buffered.getvalue()))
        im.close()
        instance.raw_data_ready = True
        instance.save()
