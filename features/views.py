from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from urllib.parse import urlparse

from django.contrib.auth.models import User
from . models import Paper

from . tf_idf import preprocess, create_tfidf_features, calculate_similarity, show_similar_documents
import time
import pandas as pd
from . utils import filter__in_preserve, paginate_papers, topic_distrib, paginate_papers


# Create your views here.

def landing_view(request):
    return render(request, 'features/landing.html')


def login_view(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            print("Username does not exist")

        user = authenticate(request, username=username, password=password)

        # Get current path
        current_path = urlparse(request.META.get('HTTP_REFERER')).path

        if user is not None:
            login(request, user)
            print("logged in")

            # If full path is 127.0.0.1:8000/login, redirect to home
            if current_path == '/login/':
                return redirect('home')
            else: # Else stay on current path
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        else:
            print('Username or password is incorrect')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
           
    #return render(request, 'papers/paper.html', context_instance=RequestContext(request))
    #return redirect(request.path)
    return render(request, 'features/login.html')
    

def logout_view(request):
    logout(request)
    return redirect('landing')


def results_view(request):
    search = ""

    if request.method == 'GET' and 'search' in request.GET:
        search = request.GET['search']
        
        if search:

            #get the corpus
            corpus = Paper.objects.values('title', 'abstract')

            # If corpus is not None, process corpus
            res = [ele for ele in corpus]

            if bool(res) is not False: 

                corpus_list = [entry for entry in corpus] 

                df = pd.DataFrame(corpus_list, columns=["title", "abstract"])
                print(df)
                
                # preprocess the corpus
                data = [preprocess(title, abstract) for title, abstract in zip(df['title'], df['abstract'])]

                # Learn vocabulary and idf, return term-document matrix
                X,v = create_tfidf_features(data)
                features = v.get_feature_names_out()
                #print(features, len(features))

                #run
                user_question = [search]
                search_start = time.time()
                sim_vecs, cosine_similarities = calculate_similarity(X, v, user_question)
                search_time = time.time() - search_start
                print("search time: {:.2f} ms".format(search_time * 1000))
                print()
            
                 # show similary and documents
                search_num = show_similar_documents(data, cosine_similarities, sim_vecs)


                abstract_list = []

                if search_num != 0:
                    for i in cosine_similarities.argsort()[-search_num:][::-1]:
                        #print(df.iloc[i, 0])
                        abstract_list.append(df.iloc[i, 1])
                
                #papers = Paper.objects.filter(abstract__in=abstract_list)
                papers = filter__in_preserve(Paper.objects, 'abstract', abstract_list).all()
                custom_range, papers = paginate_papers(request, papers, 4)

            else:
                papers = Paper.objects.all()
                custom_range, papers = paginate_papers(request, papers, 4)

        else:
            # empty search
            papers = Paper.objects.all()
            custom_range, papers = paginate_papers(request, papers, 4)

    else:
        # no search
        papers = Paper.objects.all()
        custom_range, papers = paginate_papers(request, papers, 4)

    context = {'papers': papers, 'search': search, 'custom_range': custom_range}
    return render(request, 'features/home.html', context)


def home_view(request):
    search = ""

    # no search
    papers = Paper.objects.all()

    custom_range, papers = paginate_papers(request, papers, 4)

    context = {'papers': papers, 'search': search, 'custom_range': custom_range}
    return render(request, 'features/home.html', context)


def paper_view(request, slug):
    paper = Paper.objects.get(slug=slug)

    # current paper title, abstract
    current_title = paper.title
    current_abstract = paper.abstract
    
    # current paper topic distrib
    current_topic_distrib = topic_distrib(current_abstract)
    print(current_topic_distrib)

    
    # get all corpus title and abstracts
    corpus = Paper.objects.values('title', 'abstract').exclude(title=current_title)
 
    corpus_list = [entry for entry in corpus] 

    df = pd.DataFrame(corpus_list, columns=["title", "abstract"])
    print(df)

    # loop through each check each first index topic distributions
    title_list = []

    for index in current_topic_distrib: # [1, 0, 5]
        for title, abstract in zip(df['title'], df['abstract']):
            loop_topic_distrib = topic_distrib(abstract) # get topic distrib for each doc [1, 0, 6], [1, 0, 5]

            if loop_topic_distrib[0] == index:
                print(loop_topic_distrib)
                title_list.append(title)

        
    related_papers = filter__in_preserve(Paper.objects, 'title', title_list).all()

    #custom_range, related_papers = paginate_papers(request, related_papers, 2)

    context = {'paper': paper, 'related_papers': related_papers}
    return render(request, 'features/paper.html', context)