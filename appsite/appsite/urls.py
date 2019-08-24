from django.contrib import admin
from django.urls import path, include

import resolver.urls

openapi_urlpatterns = [
    path('', include(resolver.urls))
]


from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Prototype API', patterns=openapi_urlpatterns)

import rest_framework.urls


urlpatterns = [
    path('openapi/', schema_view),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(resolver.urls)),
]


