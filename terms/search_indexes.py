from haystack.indexes import SearchIndex, CharField, EdgeNgramField
from .models import Term


class TermIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='original_name')

    def get_model(self):
        return Term


import haystack
version = haystack.__version__[0]
if version == 2:
    from haystack.indexes import Indexable
    class TermIndex(TermIndex, Indexable):
        pass
elif version == 1:
    haystack.site.register(Term, TermIndex)
