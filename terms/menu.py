from cms.menu_bases import CMSAttachMenu
from django.core.urlresolvers import NoReverseMatch
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
        for term in Term.objects.all():
            try:
                node = NavigationNode(
                    smart_text(term),
                    term.get_absolute_url(),
                    term.pk,
                )
                nodes.append(node)
            except NoReverseMatch:
                pass
        return nodes


menu_pool.register_menu(TermsMenu)
