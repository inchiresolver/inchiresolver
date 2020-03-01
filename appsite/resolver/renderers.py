from rest_framework.renderers import TemplateHTMLRenderer, BrowsableAPIRenderer
import os


class ResolverAPIRenderer(BrowsableAPIRenderer):

    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(data, accepted_media_type, renderer_context)
        if os.environ['INCHI_RESOLVER_TITLE'] == '':
            context['resolver_title'] = 'InChI Resolver'
        else:
            context['resolver_title'] = os.environ.get('INCHI_RESOLVER_TITLE', 'InChI Resolver')
        if os.environ['INCHI_RESOLVER_COLOR_SCHEME'] == '':
            context['resolver_color_scheme'] = 'inchi-resolver-default-color-scheme'
        else:
            context['resolver_color_scheme'] = os.environ.get('INCHI_RESOLVER_COLOR_SCHEME', 'inchi-resolver-default-color-scheme')
        return context