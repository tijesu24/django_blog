# Generated by Django 5.0.4 on 2024-06-16 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_comment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to='media/% Y/% m/% d/'),
        ),
    ]
