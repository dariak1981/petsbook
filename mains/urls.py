from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.conf.urls.i18n import i18n_patterns

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# if settings.DEBUG:
#     urlpatterns += staticfiles_urlpatterns()


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('register/', user_views.register, name='register'),
    path('listings/', include('listings.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
