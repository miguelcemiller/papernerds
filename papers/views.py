from django.shortcuts import render
from . models import Paper
from django.db.models import Q

from . boyermoore import boyer_moore_horspool


def homeView(request):

    search = ""

    if request.method == 'GET' and 'search' in request.GET:
        search = request.GET['search']
        #papers = Paper.objects.all().filter(abstract__icontains=search) #filter papers first based on abstract # only works with one word or 2 words together
        if search:
            q = None
            for word in search.split():
                q_aux = Q(title__icontains = word) | Q(abstract__icontains = word)
                q = ( q_aux & q ) if bool( q ) else q_aux

            papers = Paper.objects.filter(q)
        else:
            papers = Paper.objects.all()  
    else:
        papers = Paper.objects.all()

    context = {'papers': papers, 'search': search }
    return render(request, 'papers/home.html', context)






    
