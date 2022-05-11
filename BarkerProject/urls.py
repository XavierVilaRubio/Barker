"""BarkerProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib.auth.views import LogoutView, LoginView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from BarkerApp import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/users', views.UserViewSet)
router.register(r'api/profiles', views.ProfileViewSet)
router.register(r'api/requests', views.RequestViewSet)
router.register(r'api/barks', views.BarkViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # VIEWS
    path('index/', views.index_view, name='index'),
    path('home/', views.home_view, name='home'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('requests/', views.requests_view, name='requests'),
    path('follow/<username>/', views.send_request, name='follow'),
    path('unfollow/<username>/', views.unfollow, name='unfollow'),
    path('accept/<username>/', views.accept_request, name='accept'),
    path('cancel/<username>/', views.cancel_request, name='cancel'),
    path('post_bark/', views.post_bark, name='post_bark'),
    path('bark/<int:bark_id>/', views.barkView, name='bark'),
    path('barks/<int:bark_id>/', views.get_bark, name='bark'),
    path('delete_bark/<int:bark_id>/', views.delete_bark, name='delete_bark'),
    path('edit_bark/<int:bark_id>/', views.edit_bark, name='edit_bark'),
    path('reply_bark/<int:bark_id>/', views.reply_bark, name='reply_bark'),
    path('<username>/', views.get_profile_view, name='profile'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)