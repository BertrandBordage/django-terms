from django.views.generic import DetailView
from .models import Term


class TermDetail(DetailView):
    model = Term
    context_object_name = 'term'
