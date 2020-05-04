from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice, News


def index(request):
    return HttpResponse("Hello, world. You're at the start page.")

def poll_index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return  render(request,'poll/poll_index.html',context)

class PollIndexView(generic.ListView):
    template_name = 'poll/poll_index.html'
    context_object_name =  'latest_question_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class NewsIndexView(generic.ListView):
    template_name = 'news_index.html'
    context_object_name =  'latest_news'
    def get_queryset(self):
        # return News.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:10]
        return News.objects.all().order_by('-pub_date')[:10]



class PollDetailView(generic.DetailView):
    model = Question
    template_name = 'poll/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class PollResultsView(generic.DetailView):
    model = Question
    template_name = 'poll/results.html'


def poll_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/detail.html', {'question': question})

def poll_results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {'question': question})

def poll_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'poll/detail.html', {
            'question': question,
            'error_message':'Ви не вибрали відповідь'})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('poll_results', args=(question.id,)))

