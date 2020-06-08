from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Q
from math import log2, pow

from .models import Question, Choice, News, Match,Tourney, Tourney_Group, Tourney_Group_Player, Myimage


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
    last_resusts_list = last_resusts_list[:30]
    return render(request, 'results/last30.html', {'last_resusts_list': last_resusts_list})

def tourney_index(request):
    tourney_list = Tourney.objects.all().order_by('-dt')
    tourney_list = tourney_list[:20]
    return render(request, 'tourney/index.html', {'tourney_list': tourney_list})

def tourney_detail(request, tid):
    tourney = get_object_or_404(Tourney, pk=tid)
    last_resusts_list = Match.objects.filter(tourney_group__tourney_id=tid).order_by('-dt')
    last_resusts_list = last_resusts_list[:40]
    context = {
        'tourney': tourney,
        'last_resusts_list':last_resusts_list,
    }
    return  render(request,'tourney/detail.html',context)

def get_table_group_by_id(gid):
    tourney_group = get_object_or_404(Tourney_Group, pk=gid)
    n_players =tourney_group.n_players
    players = Tourney_Group_Player.objects.filter(tourney_group=gid).order_by('nn')
    tg = []
    i = 1
    y = [tourney_group.name,'Гравці']
    for k in range(n_players):
        y.append(str(k+1))
    y.append('Ігри')
    y.append('Бали')
    y.append('Сети')
    y.append('Гейми')
    tg.append(y)
    for p in players:
        y = [str(i),str(p.player)]
        matches, points,sets1,sets2, games1,games2 = 0,0,0,0,0,0
        for p1 in players:
            if p1.id == p.id:
                y.append('x')
            else:
                m1 = Match.objects.filter(tourney_group_id=gid, player1_id= p.player_id, player2_id=p1.player_id)
                m2 = Match.objects.filter(tourney_group_id=gid, player1_id=p1.player_id, player2_id= p.player_id)
                if len(m1)>0:
                    m=m1[0]
                    matches+=1
                    if m.s1>m.s2:
                        points +=1
                    elif (m.withdrawal and m.winner==1):
                        points += 1

                    sets1 += m.s1
                    sets2 += m.s2
                    games1 += m.g1
                    games2 += m.g2
                    y.append(m.rezs1())
                elif len(m2)>0:
                    m = m2[0]
                    matches += 1
                    if m.s1 < m.s2:
                        points += 1
                    elif (m.withdrawal and m.winner == 2):
                        points += 1
                    sets1 += m.s2
                    sets2 += m.s1
                    games1 += m.g2
                    games2 += m.g1
                    y.append(m.rezs2())
                else:
                    y.append('-')
        y.append(str(matches))
        y.append(str(points))
        y.append(str(sets1) + '-' +str(sets2))
        y.append(str(games1) + '-' + str(games2))


        i=i+1
        tg.append(y)
    return tg

def get_pf_by_id(gid):
    tourney_group = get_object_or_404(Tourney_Group, pk=gid)
    n_round = round(log2(tourney_group.n_players))
    h = ['1/16','1/8','1/4','1/2','Фінал']
    h = h[-n_round:]
    pf=[]
    perc = 100
    for i in range(n_round):
        y=[]
        n_plaers = round( pow(2,i))
        for j in range(n_plaers):
            r = {}
            m1 = Match.objects.filter(tourney_group_id=gid,group_id=n_plaers+j)
            if len(m1) > 0:
                m = m1[0]
                r['p'] = m.pp()
                r['r'] = m.rezs1()
                r['p1'] = m.pplayer1()
                r['p2'] = m.pplayer2()
                r['perc'] = perc
                r['i'] =  n_round - i
                y.append(r)
            else:
                r['p'] =' '
                r['r'] = ''
                r['p1'] = ''
                r['p2'] = ''
                r['perc'] = perc
                r['i'] = n_round - i
                y.append(r)
        perc = perc // 2
        pf.insert(0,y)
    return pf

def tourney_group_detail(request,tid, gid):
    tourney_group = get_object_or_404(Tourney_Group, pk=gid)
    tourney = get_object_or_404(Tourney, pk=tid)
    tg = get_table_group_by_id(gid)
    pf = get_pf_by_id(gid)
    last_resusts_list = Match.objects.filter(tourney_group_id=gid).order_by('-dt')
    context = {
        'pf':pf,
        'tourney':tourney,
        'tourney_group_head': tg[:1],
        'tourney_group_body': tg[1:],
        'tourney_group':tourney_group,
        'last_resusts_list':last_resusts_list,
    }
    return  render(request,'tourney/group_detail.html',context)

def foto_index(request):
    foto_list = Myimage.objects.all().order_by('-dt')
    foto_list = foto_list[:10]
    return render(request, 'foto/index.html', {'foto_list': foto_list})

def foto_detail(request, pk):
    foto = get_object_or_404(Myimage, pk=pk)
    context = {
        'foto': foto,
    }
    return  render(request,'foto/detail.html',context)