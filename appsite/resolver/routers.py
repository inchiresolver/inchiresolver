from rest_framework import routers

from resolver.views import ResolverApiView


class ResolverApiRouter(routers.DefaultRouter):
    APIRootView = ResolverApiView
