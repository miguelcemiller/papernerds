from django.db.models.expressions import Case, When
from django.db.models.query import QuerySet
from django.shortcuts import render
from . models import Paper
from django.db.models import Q
from django.db.models import F
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from collections import OrderedDict

from . boyermoore import boyer_moore_horspool
from . tf_idf import preprocess, create_tfidf_features, calculate_similarity, show_similar_documents

import time
import pandas as pd


def homeView(request):

    search = ""

    if request.method == 'GET' and 'search' in request.GET:
        search = request.GET['search']
        
        if search:
            #get the corpus
            corpus_abstracts = Paper.objects.values_list('abstract', flat=True)

            df = pd.DataFrame(corpus_abstracts, columns=["abstract"])

            #preprocess the corpus
            data = [preprocess(abstract) for abstract in df['abstract']]

            # Learn vocabulary and idf, return term-document matrix
            X,v = create_tfidf_features(data)
            features = v.get_feature_names_out()

            #run
            user_question = [search]
            search_start = time.time()
            sim_vecs, cosine_similarities = calculate_similarity(X, v, user_question)
            search_time = time.time() - search_start
            print("search time: {:.2f} ms".format(search_time * 1000))
            print()
           

           # show similary and documents
            search_num = show_similar_documents(data, cosine_similarities, sim_vecs)

            # to set list in order when filtered in model
            def filter__in_preserve(queryset: QuerySet, field: str, values: list) -> QuerySet:
                """
                .filter(field__in=values), preserves order.
                """
                # (There are not going to be missing cases, so default=len(values) is unnecessary)
                preserved = Case(*[When(**{field: val}, then=pos) for pos, val in enumerate(values)])
                return queryset.filter(**{f'{field}__in': values}).order_by(preserved)


            abstract_list = []

            if search_num != 0:
                for i in cosine_similarities.argsort()[-search_num:][::-1]:
                    #print(df.iloc[i, 0])
                    abstract_list.append(df.iloc[i, 0])
            
            #papers = Paper.objects.filter(abstract__in=abstract_list)
            papers = filter__in_preserve(Paper.objects, 'abstract', abstract_list).all()

            page = request.GET.get('page')
            paginator = Paginator(papers, 4)

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

        else:
            # empty search
            papers = Paper.objects.all()

            #p = Paginator(papers, 4)
  
    else:
        # no search
        papers = Paper.objects.all()

        page = request.GET.get('page')
        paginator = Paginator(papers, 4)

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

    context = {'papers': papers, 'search': search, 'custom_range': custom_range}
    return render(request, 'papers/home.html', context)
















# def homeView(request):

#     search = ""

#     if request.method == 'GET' and 'search' in request.GET:
#         search = request.GET['search']
#         #papers = Paper.objects.all().filter(abstract__icontains=search) #filter papers first based on abstract # only works with one word or 2 words together
#         if search:
#             q = None
#             for word in search.split(" "):
#                 # print(word)
#                 q_aux = Q(title__icontains = word) | Q(abstract__icontains = word)
#                 q = ( q_aux & q ) if bool( q ) else q_aux

#             papers = Paper.objects.filter(q)
#         else:
#             papers = Paper.objects.all()  
#     else:
#         papers = Paper.objects.all()



#     context = {'papers': papers, 'search': search }
#     return render(request, 'papers/home.html', context)






    
