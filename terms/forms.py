# coding: utf-8

from django.forms import ModelForm, CharField, Textarea, ValidationError
from .models import Term
from django.utils.translation import ugettext as _
try:
    from ckeditor.widgets import CKEditorWidget
    Textarea = CKEditorWidget()
except ImportError:
    pass


class TermForm(ModelForm):
    definition = CharField(widget=Textarea)

    def clean(self):
        definition = self.cleaned_data.get('definition')
        url = self.cleaned_data.get('url')
        if not definition and not url:
            raise ValidationError(_(u'Fill either “Definition” or “Link”.'))
        return super(TermForm, self).clean()

    class Meta:
        model = Term
