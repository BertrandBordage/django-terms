from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from .models import Term


class TermsIndexPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _('Glossary')
    render_template = 'glossary_plugin.html'

    def render(self, context, instance, placeholder):
        context['terms'] = Term.objects.all()
        return context


plugin_pool.register_plugin(TermsIndexPlugin)
