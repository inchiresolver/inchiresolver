from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

import resolver.urls

# openapi_urlpatterns = [
#     path('', include(resolver.urls))
# ]
#
# schema_view = get_swagger_view(title='Prototype API', patterns=openapi_urlpatterns)

urlpatterns = [
    path('openapi', get_schema_view(
        title="InChI Resolver",
        description="InChI Resolver",
    ), name='openapi-schema'),
    path('redoc', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
    path('swagger-ui', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('admin', admin.site.urls),
    re_path('^api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(resolver.urls)),
]


