from django.db.models.expressions import Case, When
from django.db.models.query import QuerySet
from django.shortcuts import render
from . models import Paper
from django.db.models import Q
from django.db.models import F

from collections import OrderedDict

from . boyermoore import boyer_moore_horspool


def homeView(request):

    search = ""

    if request.method == 'GET' and 'search' in request.GET:
        search = request.GET['search']
        #papers = Paper.objects.all().filter(abstract__icontains=search) #filter papers first based on abstract # only works with one word or 2 words together
        if search:
            q = None
            for word in search.split(" "):
                # print(word)
                q_aux = Q(title__icontains = word) | Q(abstract__icontains = word)
                q = ( q_aux & q ) if bool( q ) else q_aux

            papers = Paper.objects.filter(q)
        else:
            papers = Paper.objects.all()  
    else:
        papers = Paper.objects.all()

    
    # make dict
    dict = {}
    for paper_obj in papers.iterator(): # Loop through each Papers obj depending on search

        title = paper_obj.title
        index_found = boyer_moore_horspool(paper_obj.abstract, search) # returns indexes found
        count = len(index_found) # may return 0 because we search from the abstract

        dict[title] = count # add to dictionary


    sorted_dict = sorted(dict.items(), key=lambda x:x[1], reverse=True) # sort from highest to lowest
    # print(sorted_dict.count)
    # print(sorted_dict)
    print(sorted_dict[0][0]) # prints the first The lazy dog Part 4
    print(sorted_dict[1][0]) # prints the second The lazy dog Part 2
    print(sorted_dict[2][0]) # prints the thid The lazy dog Part 1

    data_list = []
    data_list.append(sorted_dict[0][0])
    data_list.append(sorted_dict[1][0])
    data_list.append(sorted_dict[2][0])

    print(data_list)

    def filter__in_preserve(queryset: QuerySet, field: str, values: list) -> QuerySet:
        """
        .filter(field__in=values), preserves order.
        """
        # (There are not going to be missing cases, so default=len(values) is unnecessary)
        preserved = Case(*[When(**{field: val}, then=pos) for pos, val in enumerate(values)])
        return queryset.filter(**{f'{field}__in': values}).order_by(preserved)



    papers = filter__in_preserve(Paper.objects, 'title', data_list).all()
        

        


    context = {'papers': papers, 'search': search }
    return render(request, 'papers/home.html', context)






    
