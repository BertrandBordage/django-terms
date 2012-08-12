from haystack.indexes import RealTimeSearchIndex , Indexable, \
                             CharField, EdgeNgramField
from .models import Term


class TermIndex(RealTimeSearchIndex, Indexable):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='name')

    def get_model(self):
        return Term
