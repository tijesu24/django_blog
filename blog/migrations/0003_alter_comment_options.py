# Generated by Django 5.0.4 on 2024-06-14 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_image_alter_comment_options_alter_post_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_on'], 'permissions': [('edit_comment_content', 'Can edit comment')]},
        ),
    ]
