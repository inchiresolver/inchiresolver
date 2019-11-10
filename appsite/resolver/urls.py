from django.urls import include, path

from rest_framework.routers import SimpleRouter

from resolver import views

# Create a router and register our viewsets with it.
router = SimpleRouter()
router.register('inchis', views.InchiViewSet)
router.register('organizations', views.OrganizationViewSet)
router.register('publishers', views.PublisherViewSet)
router.register('entrypoints', views.UrlEntryPointViewSet)
router.register('endpoints', views.UriEndPointViewSet)
urlpatterns = router.urls

#urlpatterns += path('', views.api_root)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
#urlpatterns = [
#    path(r'^', include(router.urls, 'resolver')),
#    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
#]