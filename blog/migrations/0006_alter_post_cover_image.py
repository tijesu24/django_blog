# Generated by Django 5.0.4 on 2024-06-16 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to='%Y/%m/%d/'),
        ),
    ]