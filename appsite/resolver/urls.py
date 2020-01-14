from django.conf.urls import url
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from resolver import views
#from views import InchiRelationshipView

router = DefaultRouter(trailing_slash=False)
router.register('inchis', views.InchiViewSet)
#router.register('inchikeys', views.InchiKeyViewSet)
router.register('organizations', views.OrganizationViewSet)
router.register('publishers', views.PublisherViewSet)
router.register('entrypoints', views.EntryPointViewSet)
router.register('endpoints', views.EndPointViewSet)
urlpatterns = router.urls

urlpatterns = urlpatterns + [
    url(
        regex=r'^inchis/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=views.InchiRelationshipView.as_view(),
        name='inchi-relationships'
    )
]
#urlpatterns = urlpatterns + [path('', views.api_root),]


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
#urlpatterns = [
#    path(r'^', include(router.urls, 'resolver')),
#    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
#]