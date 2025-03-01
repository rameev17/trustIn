
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('backend/', include([
        path('admin/', admin.site.urls),
        path('trustIn/', include('trustIn.urls')),
        path('shop/', include('shop.urls')),
        path('subscription/', include('subscription.urls')),
        path('projects/', include('projects.urls')),
    ]))
]