from django.shortcuts import render
from . models import Paper

from . boyermoore import boyer_moore_horspool

def homeView(request):

    paper_indexes_list = []
    is_search = False

    if 'search' in request.GET:
        is_search = True

        search = request.GET['search']
        papers = Paper.objects.all().filter(abstract__icontains=search) #filter papers first based on abstract

        search_len = len(search) # length of search
 
        for paper in papers: # loop through each papers
            abstract = paper.abstract # get the abstract
            results = boyer_moore_horspool(abstract, search) # this will return all starting indexes from abstract

            indexes = []

            for start_index in results: # loop through each starting indexes
                end_index = start_index + search_len # get last index

                start_end_index = []   # [4, 7]
                start_end_index.extend((start_index, end_index)) # [4, 7]

                indexes.append(start_end_index)
        
            paper_indexes_list.append(indexes)
        
        
        print(paper_indexes_list[0])

    else:
        papers = Paper.objects.all()


    context = {'papers': papers, 'indexes': paper_indexes_list, 'is_search': is_search }
    return render(request, 'papers/home.html', context)






    
