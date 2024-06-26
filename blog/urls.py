from . import views
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from .feeds import LatestPostsFeed
from django.contrib.auth import views as auth_views

from django.views.static import serve


sitemaps = {
    "posts": PostSitemap,
}

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),

    path("ckeditor5/", include('django_ckeditor_5.urls')),
    # path('summernote/', include('django_summernote.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("register/", views.register, name="register"),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change_password'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    path('<slug:slug>/', views.post_detail, name='post_detail'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    # serving media files only on debug mode
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]
