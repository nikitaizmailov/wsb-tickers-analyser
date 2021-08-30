# needed to respond back with a HTML template with data inside
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, response

from django.urls import reverse

# Just a basic response when sending a request to this url
from django.http import HttpResponse

from django.views.generic import TemplateView
from matplotlib.pyplot import plot

from .models import Subreddit, Comment, SubredditForm

# django's builtin datetime awareness handling lib
from django.utils import timezone

from .reddit_analyser import plot_graph, generate_subreddit

# defining a function that will be called out when the request is send
# to a url path

# Using class it inherits methods from class VIEW which handles the linking the view into the URLs
# HTTP method dispatching and other common features
class HomeView(TemplateView):
    template_name = 'wsb/homepage.html'

    # below defining context parameters that will be passed to the url and template
    # get_context_data function will define for you a dictionary to which you can assign
    # as many parameters as you want to pass into the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_subreddits'] = Subreddit.objects.order_by('-id')[:5]
        context['form'] = SubredditForm()
        return context

def about_me(request):
    return render(request, 'wsb/about_me.html', {})

def detail(request, subreddit_id):
    try:
        subr = Subreddit.objects.get(id=subreddit_id)
    except Subreddit.DoesNotExist:
        raise Http404("Subreddit does not exist")

    latest_comments = subr.comment_set.order_by('-id')[:10]

    return render(request, 'wsb/detail.html', {"subr": subr, "latest_comments":latest_comments,})

def leave_comment(request, subreddit_id):
    try:
        s = Subreddit.objects.get(id=subreddit_id)
    except:
        raise Http404("Subreddit not found")

    s.comment_set.create(author_name = request.POST['name'], comment_text=request.POST['text'])

    return HttpResponseRedirect(reverse('wsb:detail', args=(s.id,)))

def create_q(request):
    if request.method == "POST":
        s = Subreddit(subreddit_name=request.POST['subreddit_name'], submission_title=request.POST['submission_title'], 
                    regex_pattern=request.POST['regex_pattern'], 
                    post_date=timezone.now())
        s.save()

        if request.POST.get('generate_analysis_button', False):
            return results(request, s)
        elif request.POST.get('last_comments_button', False):
            return HttpResponseRedirect(reverse('wsb:home'))
        else:
            pass

# Below function generate analysis and displays them on the page.
def results(request, dict_things=None):
    object_dict = dict_things
    
    context={
        'object_dict':object_dict,
    }

    #generating the input from the passed data in the request dictionary
    if object_dict:
        # the first three statements below are generating input vars for the plot_graph function. So don't worry and be happy!
        regex_pattern = object_dict.regex_pattern
        subr_object, subms, sub_titles_ids = generate_subreddit(object_dict.subreddit_name)
        submission_title_selected = object_dict.submission_title

        plot_chart = plot_graph(regex_pattern, subr_object, subms, sub_titles_ids, submission_title_selected)

        context['chart'] = plot_chart[0]

        context['comments'] = plot_chart[1]

        context['comms_extracted'] = plot_chart[2]

        context['regex_pattern'] = plot_chart[3]

    

    return render(request, 'wsb/results.html', context)