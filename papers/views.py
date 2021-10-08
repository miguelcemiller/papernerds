from django.shortcuts import render
from . models import Paper

def homeView(request):
    papers = Paper.objects.all()
    context = {'papers': papers}

    return render(request, 'papers/home.html', context)
