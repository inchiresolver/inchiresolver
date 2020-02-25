from rest_framework.renderers import TemplateHTMLRenderer, BrowsableAPIRenderer
import os

class ResolverAPIRenderer(BrowsableAPIRenderer):

    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(data, accepted_media_type, renderer_context)
        context['navbar_title'] = os.environ['INCHI_RESOLVER_NAVBAR_TITLE']
        context['navbar_color'] = os.environ['INCHI_RESOLVER_NAVBAR_COLOR']
        return context