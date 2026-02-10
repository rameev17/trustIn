
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from trustIn import views as trustIn_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/', include([
        path('about/', trustIn_views.about_view, name='about'),
        path('team/', trustIn_views.team_view, name='team'),
        path('trustIn/', include('trustIn.urls')),
        path('shop/', include('shop.urls')),
        path('subscription/', include('subscription.urls')),
        path('projects/', include('projects.urls')),
    ]))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
