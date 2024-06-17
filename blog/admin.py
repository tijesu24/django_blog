from django.shortcuts import render
from django.urls import path
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import STATUS, Post
from django.contrib import admin

from django.db import models
from image_uploader_widget.widgets import ImageUploaderWidget

# Register your models here.
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment


# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'status', 'created_on')
#     list_filter = ("status",)
#     search_fields = ['title', 'content']
#     prepopulated_fields = {'slug': ('title',)}

#     inlines = [CommentInline]


# admin.site.register(Post, PostAdmin)


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'body', 'post', 'created_on', 'active')
#     list_filter = ('active', 'created_on')
#     search_fields = ('name', 'email', 'body')
#     actions = ['approve_comments', 'disapprove_comments']

#     def approve_comments(self, request, queryset):
#         queryset.update(active=True)

#     def disapprove_comments(self, request, queryset):
#         queryset.update(active=False)

#     def get_readonly_fields(self, request, obj=None):
#         readonly_fields = []  # Always make 'active' field editable
#         if not request.user.has_perm('blog.edit_comment_content'):
#             readonly_fields.extend(
#                 ['name', 'email', 'body', 'post', 'created_on'])
#         return readonly_fields


class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    inlines = [CommentInline]

    formfield_overrides = {
        models.ImageField: {'widget': ImageUploaderWidget},
    }

    def has_change_permission(self, request, obj=None):
        if obj and request.user.has_perm('blog.change_post'):
            return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and request.user.has_perm('blog.delete_post'):
            return True
        return super().has_delete_permission(request, obj)

    actions = ['publish_publication', "send_publication_to_drafts"]

    def publish_publication(self, request, queryset):
        queryset.update(status=1)

    def send_publication_to_drafts(self, request, queryset):
        queryset.update(status=0)


admin.site.register(Post, PostAdmin)


class UserAdmin(BaseUserAdmin):
    actions = ["add_to_blog_managers"]

    def add_to_blog_managers(modeladmin, request, queryset):
        # Get the Blog Managers group
        try:
            blog_managers_group = Group.objects.get(name='Blog Managers')
        except Group.DoesNotExist:
            messages.error(request, 'Blog Managers group does not exist.')
            return

        # Update selected users
        for user in queryset:
            user.groups.add(blog_managers_group)
            user.is_staff = True
            user.save()

        # Notify the admin user about the update
        messages.success(
            request, 'Selected users have been added to the Blog Managers group and granted staff status.')

    add_to_blog_managers.short_description = "Make user a Blog Manager"

    #  Add a custom method to check if a user is in the Blog Managers group
    def is_blog_manager(self, obj):
        return obj.groups.filter(name='Blog Managers').exists()
    is_blog_manager.boolean = True  # Display as a boolean icon
    is_blog_manager.short_description = 'Blog Manager'  # Column name

    # Extend the list display to include the new method
    list_display = BaseUserAdmin.list_display + ('is_blog_manager',)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class CustomCommentAdmin(admin.ModelAdmin):
    change_list_template = 'admin/comments_by_post.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('comments-by-post/', self.admin_site.admin_view(
                self.comments_by_post_view), name='comments-by-post'),
        ]
        return custom_urls + urls

    def comments_by_post_view(self, request):
        posts = Post.objects.prefetch_related('comments').all()
        context = dict(
            self.admin_site.each_context(request),
            posts=posts,
        )
        return render(request, 'admin/comments_by_post.html', context)


admin.site.register(Comment, CustomCommentAdmin)
