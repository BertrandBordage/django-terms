# -*- coding: utf-8 -*-
import terms.templatetags
import terms.templatetags.terms
import terms.admin
import terms.cms_apps
import terms.cms_plugin_processors
import terms.cms_plugins
import terms.forms
import terms.html
import terms.managers
import terms.menu
import terms.middleware
import terms.models
import terms.search_indexes
import terms.settings
import terms.sitemaps
import terms.urls
import terms.views


def test_import_terms():
    assert terms.templatetags
    assert terms.templatetags.terms
    assert terms.admin
    assert terms.cms_apps
    assert terms.cms_plugin_processors
    assert terms.cms_plugins
    assert terms.forms
    assert terms.html
    assert terms.managers
    assert terms.menu
    assert terms.middleware
    assert terms.models
    assert terms.search_indexes
    assert terms.settings
    assert terms.sitemaps
    assert terms.urls
    assert terms.views
