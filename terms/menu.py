from cms.menu_bases import CMSAttachMenu
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from django.core.urlresolvers import NoReverseMatch
from .models import Term
from django.utils.translation import ugettext_lazy as _


class TermMenu(CMSAttachMenu):
    name = _('Term Menu')

    def get_nodes(self, request):
        '''
        This method is used to build the menu tree.
        '''
        nodes = []
        for term in Term.objects.iterator():
            try:
                node = NavigationNode(
                    unicode(term),
                    term.get_absolute_url(),
                    term.pk,
                )
                nodes.append(node)
            except NoReverseMatch:
                pass
        return nodes


menu_pool.register_menu(TermMenu)
