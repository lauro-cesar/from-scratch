# Generated by Django 3.2.8 on 2021-12-02 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restfiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restimagemodel',
            name='original',
            field=models.ImageField(default='eca.png', upload_to='restimages/originals/', verbose_name='Original'),
            preserve_default=False,
        ),
    ]
