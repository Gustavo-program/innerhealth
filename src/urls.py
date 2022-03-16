from django.contrib import admin
from django.urls import include, path
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('inner-health/', include('core.urls')),
]
