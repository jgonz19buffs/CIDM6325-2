"""
URL configuration for myshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from blog.sitemaps import PostSitemap,TagSitemap
from payment import webhooks

sitemaps = {
    'posts': PostSitemap,
    'tags': TagSitemap,
}

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path(_('account/'), include('account.urls')),
    path(_('blog/'), include('blog.urls',namespace='blog')),
    path(_('cart/'), include('cart.urls', namespace='cart')),
    path(_('images/'), include('images.urls', namespace='images')),
    path(_('orders/'), include('orders.urls', namespace='orders')),
    path(_('payment/'), include('payment.urls', namespace='payment')),
    path(_('coupons/'), include('coupons.urls', namespace='coupons')),
    path('rosetta/', include('rosetta.urls')),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path(
        'social-auth/',
        include('social_django.urls', namespace='social')
    ),
    path('', include('shop.urls', namespace='shop')),
)

urlpatterns += [
    path(
        'webhook/',
        webhooks.stripe_webhook,
        name='stripe-webhook'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )