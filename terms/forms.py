# coding: utf-8

from django.forms import ModelForm, ValidationError
from .models import Term
from django.utils.translation import ugettext as _


class TermForm(ModelForm):
    def clean(self):
        definition = self.cleaned_data.get('definition')
        url = self.cleaned_data.get('url')
        if not definition and not url:
            raise ValidationError(_(u'Fill either “Definition” or “Link”.'))
        return super(TermForm, self).clean()

    class Meta:
        model = Term
