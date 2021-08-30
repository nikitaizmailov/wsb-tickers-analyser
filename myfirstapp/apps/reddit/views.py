from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse

from django.urls import reverse

# remember that models are tables in the database that you retrieve data from
# hence why if we want to display the data we recieved from the users we need to import
from .models import Article, Comment


# below are views specifically for stock charts
def chart(request):
    
    return render(request, 'reddit/analyser.html')



def index(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:5]
    return render(request, 'reddit/list.html', {'latest_articles_list':latest_articles_list})

def detail(request, article_id):
    try:
        a = Article.objects.get(id=article_id)
    except:
        raise Http404("Article not found")
    
    latest_comments_list = a.comment_set.order_by('-id')[:10]

    # passing in request, template, then the arguments that you would want to use in template
    return render(request, 'reddit/detail.html', {'article':a, 'latest_comments_list':latest_comments_list})

def leave_comment(request, article_id):
    try:
        a = Article.objects.get(id=article_id)
    except:
        raise Http404("Article not found")

    a.comment_set.create(author_name = request.POST['name'], comment_text=request.POST['text'])

    return HttpResponseRedirect(reverse('reddit:detail', args=(a.id,)))