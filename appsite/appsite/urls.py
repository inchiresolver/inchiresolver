from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework_swagger.views import get_swagger_view

import resolver.urls

openapi_urlpatterns = [
    path('', include(resolver.urls))
]

schema_view = get_swagger_view(title='Prototype API', patterns=openapi_urlpatterns)

urlpatterns = [
    path('openapi/', schema_view),
    path('admin/', admin.site.urls),
    re_path('^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(resolver.urls)),
]


