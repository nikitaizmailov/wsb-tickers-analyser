# needed to respond back with a HTML template with data inside
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, response

from django.urls import reverse

# Just a basic response when sending a request to this url
from django.http import HttpResponse

from .models import Question, Choice


# defining a function that will be called out when the request is send
# to a url path
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'stocks/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'stocks/detail.html', {"question": question})

def vote(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'stocks/detail.html', {
            "question":question,
            "error_message": "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # reverse function is useful so that you don't need to hardcode
        # the URL in the view to point to.
        return HttpResponseRedirect(reverse('stocks:results', args=(question.id,)))

def results(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'stocks/results.html', {'question': question})
