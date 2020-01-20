from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from resolver import views

router = DefaultRouter(trailing_slash=False)
router.register('inchis', views.InchiViewSet)
router.register('organizations', views.OrganizationViewSet)
router.register('publishers', views.PublisherViewSet)
router.register('entrypoints', views.EntryPointViewSet)
router.register('endpoints', views.EndPointViewSet)

urlpatterns =  [
    re_path(r'^', include(router.urls)),

    re_path(r'^inchis/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=views.InchiRelationshipView.as_view(),
        name='inchi-relationships'
    ),
    path('inchis/<pk>/<related_field>',
        view=views.InchiViewSet.as_view({'get': 'retrieve_related'}),
        name='inchi-related'),

    re_path(r'^publishers/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=views.PublisherRelationshipView.as_view(),
        name='publisher-relationships'
    ),
    path('publishers/<pk>/<related_field>',
        view=views.PublisherViewSet.as_view({'get': 'retrieve_related'}),
        name='publisher-related'),


    re_path(r'^entrypoints/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=views.EntryPointRelationshipView.as_view(),
        name='entrypoint-relationships'
    ),
    path('entrypoints/<pk>/<related_field>',
        view=views.EntryPointViewSet.as_view({'get': 'retrieve_related'}),
        name='entrypoint-related'),


    re_path(r'^organizations/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=views.OrganizationRelationshipView.as_view(),
        name='organization-relationships'
    ),
    path('organizations/<pk>/<related_field>',
        view=views.OrganizationViewSet.as_view({'get': 'retrieve_related'}),
        name='organization-related'),


]
