from haystack.indexes import RealTimeSearchIndex, CharField, EdgeNgramField
from .models import Term


class TermIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    content_auto = EdgeNgramField(model_attr='original_name')

    def get_model(self):
        return Term
