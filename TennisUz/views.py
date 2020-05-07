from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice, News, Match,Tourney, Tourney_Group


def index(request):
    question = 1
    return render(request, 'index.html', {'question': question})


def poll_index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return  render(request,'poll/poll_index.html',context)

def tourney_spring2020(request):
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

class LastResultsView(generic.ListView):
    template_name = 'results/last30.html'
    context_object_name =  'last_resusts_list'
    def get_queryset(self):
        return Match.objects.all().order_by('-dt')

def last_results(request):
    last_resusts_list = Match.objects.all().order_by('-dt')
    last_resusts_list = last_resusts_list[:40]
    return render(request, 'results/last30.html', {'last_resusts_list': last_resusts_list})

def tourney_index(request):
    tourney_list = Tourney.objects.all().order_by('-dt')
    tourney_list = tourney_list[:10]
    return render(request, 'tourney/index.html', {'tourney_list': tourney_list})

def tourney_detail(request, tid):
    tourney = get_object_or_404(Tourney, pk=tid)

    context = {
        'tourney': tourney,
    }
    return  render(request,'tourney/detail.html',context)

def tourney_group_detail(request,tid, gid):
    tourney_group = get_object_or_404(Tourney_Group, pk=gid)
    context = {
        'tourney_group': tourney_group,
    }
    return  render(request,'tourney/group_detail.html',context)