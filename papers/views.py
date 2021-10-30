from django.shortcuts import render
from . models import Paper
from . tf_idf import preprocess, create_tfidf_features, calculate_similarity, show_similar_documents
import time
import pandas as pd
from . utils import filter__in_preserve, paginate_papers, topic_distrib, paginate_papers

 
def homeView(request):
    search = ""

    if request.method == 'GET' and 'search' in request.GET:
        search = request.GET['search']
        
        if search:
            #get the corpus
            corpus = Paper.objects.values('title', 'abstract')

            corpus_list = [entry for entry in corpus] 

            df = pd.DataFrame(corpus_list, columns=["title", "abstract"])
            print(df)
            
            # preprocess the corpus
            data = [preprocess(title, abstract) for title, abstract in zip(df['title'], df['abstract'])]

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


            abstract_list = []

            if search_num != 0:
                for i in cosine_similarities.argsort()[-search_num:][::-1]:
                    #print(df.iloc[i, 0])
                    abstract_list.append(df.iloc[i, 1])
            
            #papers = Paper.objects.filter(abstract__in=abstract_list)
            papers = filter__in_preserve(Paper.objects, 'abstract', abstract_list).all()

            custom_range, papers = paginate_papers(request, papers)

        else:
            # empty search
            papers = Paper.objects.all()

            custom_range, papers = paginate_papers(request, papers)
  
    else:
        # no search
        papers = Paper.objects.all()

        custom_range, papers = paginate_papers(request, papers)

    context = {'papers': papers, 'search': search, 'custom_range': custom_range}
    return render(request, 'papers/home.html', context)



def paperView(request, pk):
    paper = Paper.objects.get(id=pk)

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

    for title, abstract in zip(df['title'], df['abstract']):
        loop_topic_distrib = topic_distrib(abstract)
        
        if loop_topic_distrib[0] == current_topic_distrib[0]:
            #print(title)
            #print(all_topic_distrib, abs)
            title_list.append(title)
            

    related_papers = filter__in_preserve(Paper.objects, 'title', title_list).all()
        

    context = {'paper': paper, 'related_papers': related_papers}
    return render(request, 'papers/paper.html', context)












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






    
