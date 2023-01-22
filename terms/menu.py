from cms.menu_bases import CMSAttachMenu
from django.urls import NoReverseMatch
try:
    from django.utils.encoding import smart_text
except ImportError:  # For Django < 1.4.2
    from django.utils.encoding import smart_unicode as smart_text
from django.utils.translation import ugettext_lazy as _
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from .models import Term


class TermsMenu(CMSAttachMenu):
    name = _('Terms menu')

    def get_nodes(self, request):
        """
        This method is used to build the menu tree.
        """
        nodes = []
        for term in Term.objects.only('pk', 'name', 'url'):
            try:
                url = term.get_absolute_url()
            except NoReverseMatch:
                continue

            nodes.append(NavigationNode(
                smart_text(term),
                url,
                term.pk,
            ))
        return nodes


menu_pool.register_menu(TermsMenu)
