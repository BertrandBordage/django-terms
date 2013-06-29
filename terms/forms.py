# coding: utf-8

from __future__ import unicode_literals
from django.conf import settings
from django.forms import ModelForm, TextInput, ValidationError
from django.utils.translation import ugettext as _
from .models import Term
from .settings import AVAILABLE_WIDGETS, TERMS_DEFINITION_WIDGET as WIDGET

# If WIDGET == 'auto': get the best widget one can import.
# Otherwise: Get the specified widget.
if WIDGET in AVAILABLE_WIDGETS[:2]:
    from django.forms import Textarea  # 'basic'
if WIDGET == AVAILABLE_WIDGETS[2] or (WIDGET == AVAILABLE_WIDGETS[0]
                                     and 'tinymce' in settings.INSTALLED_APPS):
    from tinymce.widgets import TinyMCE as Textarea  # 'tinymce'
if WIDGET == AVAILABLE_WIDGETS[3] or (WIDGET == AVAILABLE_WIDGETS[0]
                                    and 'ckeditor' in settings.INSTALLED_APPS):
    from ckeditor.widgets import CKEditorWidget as Textarea  # 'ckeditor'


class TermForm(ModelForm):
    def clean(self):
        definition = self.cleaned_data.get('definition')
        url = self.cleaned_data.get('url')
        if not definition and not url:
            raise ValidationError(_('Fill either “Definition” or “Link”.'))
        return super(TermForm, self).clean()

    class Meta(object):
        model = Term
        widgets = {
            'name': TextInput(attrs={'size': 120}),
            'definition': Textarea(),
        }
