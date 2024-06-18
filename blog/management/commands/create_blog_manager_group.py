from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.apps import apps


class Command(BaseCommand):
    help = 'Create Blog Managers group with specific permissions'

    def handle(self, *args, **kwargs):
        # Create the group
        group, created = Group.objects.get_or_create(name='Blog Managers')

        # List of permissions to add to the group
        permissions = [
            'add_post',
            'change_post',
            'delete_post',
            'publish_post',
            'change_comment',
            'activate_comment',
            'deactivate_comment',
            'delete_comment'
        ]

        app_labels = ['easy_thumbnails', 'filer']
        all_perms_on_models = self.get_permissions_apps(app_labels)
        for perm in all_perms_on_models:
            group.permissions.add(perm)

        # Assign the permissions to the group
        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS(
            'Successfully created Blog Managers group and assigned permissions'))

    def get_permissions_apps(self, app_labels):
        permissions = Permission.objects.none()  # Start with an empty QuerySet

        for app_label in app_labels:
            app_config = apps.get_app_config(app_label)
            model_names = [
                model._meta.model_name for model in app_config.get_models()]

            for model_name in model_names:
                model_perms = Permission.objects.filter(
                    content_type__app_label=app_label,
                    content_type__model=model_name
                )
                permissions = permissions | model_perms  # Combine QuerySets

        return permissions
