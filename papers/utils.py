from django.db.models.expressions import Case, When
from django.db.models.query import QuerySet
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import gensim
import gensim.corpora as corpora


# to set list in order when filtered in model
def filter__in_preserve(queryset: QuerySet, field: str, values: list) -> QuerySet:
    """
    .filter(field__in=values), preserves order.
    """
    # (There are not going to be missing cases, so default=len(values) is unnecessary)
    preserved = Case(*[When(**{field: val}, then=pos) for pos, val in enumerate(values)])
    return queryset.filter(**{f'{field}__in': values}).order_by(preserved)


# return topic distributions for abstract
def topic_distrib(abstract):

    # load model and dict
    new_model = gensim.models.ldamodel.LdaModel.load("models/lda.model")
    lda_dict = corpora.Dictionary.load('models/lda.model.id2word')

    # topic distributions
    doc = lda_dict.doc2bow(abstract.split())
    vector = new_model.get_document_topics(doc)
    
    #print(vector)

    # sort vector
    def Sort(sub_li):
        sub_li.sort(key = lambda x:x[1])
        sub_li.reverse()
        return (sub_li)

    vector = Sort(vector)

    #print(vector) # returns sorted topic distributions

    # get only index in list
    topic_list = [item[0] for item in vector]
    #print(topic_list)

    return (topic_list)


# pagination
def paginate_papers(request, papers, items):
    page = request.GET.get('page')

    paginator = Paginator(papers, items)

    try:
        papers = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        papers = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        papers = paginator.page(page)

    left_index = (int(page) - 4)
    
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return custom_range, papers