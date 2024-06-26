# Generated by Django 5.0.4 on 2024-06-17 10:47

import django.db.models.deletion
import filer.fields.image
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_remove_post_cover_image'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover_image_3',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cover_image', to=settings.FILER_IMAGE_MODEL),
        ),
    ]
