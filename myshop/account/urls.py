from django.contrib.auth import views as auth_views
from django.urls import include,path
from django.utils.translation import gettext_lazy as _
from . import views

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path(_('register/'), views.register, name='register'),
    path(_('edit/'), views.edit, name='edit'),
    path(_('users/'), views.user_list, name='user_list'),
    path(_('users/follow/'), views.user_follow, name='user_follow'),
    path(_('user/<username>/'), views.user_detail, name='user_detail'),
]