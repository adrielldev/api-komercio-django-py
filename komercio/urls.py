from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('users.urls')),
    path('api/',include('products.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]
