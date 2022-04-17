
from django.db.models.signals import (
    pre_save,
    post_save,
    pre_init,
    post_init,
    pre_delete,
    post_delete,
    m2m_changed,
)

import hashlib
from django.dispatch import receiver
from django.conf import settings
from project.celery_tasks import app
from accounts.models import AccountProfileModel


@receiver(post_save, sender=AccountProfileModel)
def PostSaveAccountProfileModelSignals(
    sender, instance, created, using, update_fields, *args, **kwargs
):
    if True in [created]:
        for task in AccountProfileModel.TASKS.get('on_create',[]):
            app.send_task(task, [instance.id])
    else:
        for task in AccountProfileModel.TASKS.get('on_save',[]):
            app.send_task(task, [instance.id])