# Generated by Django 3.2.8 on 2021-12-02 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restfiles', '0002_restimagemodel_original'),
    ]

    operations = [
        migrations.AddField(
            model_name='restimagemodel',
            name='nome',
            field=models.CharField(default='nome', max_length=128, verbose_name='Referencia'),
            preserve_default=False,
        ),
    ]
