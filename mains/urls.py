from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.conf.urls.i18n import i18n_patterns
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('listings/', include('listings.urls')),
    path('products/', include('products.urls', namespace='products')),
    path('user/', include('users.urls')),
    path('wishlist/', include('carts.urls', namespace='carts')),
    path('support/', include('support.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('accounts.passwords.urls')),
    path('blog/', include('blog.urls')),
    path('', include('pages.urls')),
    path('marketing/', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    path('webhooks/mailchimp/', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
