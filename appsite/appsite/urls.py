from django.contrib import admin
from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Test API')

import rest_framework.urls

import resolver.urls

urlpatterns = [
    path('openapi/', schema_view),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(resolver.urls)),

]
