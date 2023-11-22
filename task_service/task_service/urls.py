from django.contrib import admin
from django.urls import include, path

from .yasg import urlpatterns as yasg_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('tasks.urls')),
]

urlpatterns += yasg_urlpatterns
