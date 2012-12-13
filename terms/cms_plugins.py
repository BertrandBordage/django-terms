from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from .models import Term


class TermsIndexPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Terms Index Plugin")
    render_template = "term_plugin.html"

    def render(self, context, instance, placeholder):
        terms = Term.objects.all()
        context['terms'] = terms
        return context


plugin_pool.register_plugin(TermsIndexPlugin)
