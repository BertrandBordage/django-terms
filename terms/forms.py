# coding: utf-8

from django.forms import ModelForm, TextInput, ValidationError
from .models import Term
from django.utils.translation import ugettext as _
from .settings import AVAILABLE_WIDGETS, TERMS_DEFINITION_WIDGET as WIDGET

# If WIDGET == 'auto': get the best widget one can import and ignore
#                      ImportError if it is raised.
# Otherwise: Get the specified widget and raises an error if not found.
try:
    if WIDGET in AVAILABLE_WIDGETS[:2]:
        from django.forms import Textarea  # 'basic'
    if WIDGET in AVAILABLE_WIDGETS[:3:2]:
        from tinymce.widgets import TinyMCE as Textarea  # 'tinymce'
    if WIDGET in AVAILABLE_WIDGETS[:4:3]:
        from ckeditor.widgets import CKEditorWidget as Textarea  # 'ckeditor'
except ImportError as e:
    if WIDGET != AVAILABLE_WIDGETS[0]:
        raise e


class TermForm(ModelForm):
    def clean(self):
        definition = self.cleaned_data.get('definition')
        url = self.cleaned_data.get('url')
        if not definition and not url:
            raise ValidationError(_(u'Fill either “Definition” or “Link”.'))
        return super(TermForm, self).clean()

    class Meta:
        model = Term
        widgets = {
            'name': TextInput(attrs={'size': 120}),
            'definition': Textarea(),
        }
