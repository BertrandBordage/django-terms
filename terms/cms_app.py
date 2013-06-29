from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from .menu import TermsMenu
from django.utils.translation import ugettext_lazy as _


class TermApp(CMSApp):
    name = _('Term')
    urls = ['terms.urls']
    menus = [TermsMenu]


apphook_pool.register(TermApp)
