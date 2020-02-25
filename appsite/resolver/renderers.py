from rest_framework.renderers import TemplateHTMLRenderer, BrowsableAPIRenderer


class ResolverAPIRenderer(BrowsableAPIRenderer):

    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(data, accepted_media_type, renderer_context)
        context['resolver_name'] = "INCHI"
        return context