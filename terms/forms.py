# coding: utf-8

from django.forms import ModelForm, ValidationError
from .models import Term
from django.utils.translation import ugettext as _


class TermForm(ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        definition = cleaned_data.get('definition')
        link = cleaned_data.get('link')
        if not definition and not link:
            raise ValidationError(_(u'Fill either “Definition” or “Link”.'))
        return super(TermForm, self).clean()

    class Meta:
        model = Term
