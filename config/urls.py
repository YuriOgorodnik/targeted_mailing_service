from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mailings.urls', namespace='mailings')),
    path('clients/', include('mailings.urls', namespace='clients')),
    path('mailings/', include('mailings.urls', namespace='mailing')),
    path('blogs/', include('blogs.urls', namespace='blogs')),
    path('users/', include('users.urls', namespace='users')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
