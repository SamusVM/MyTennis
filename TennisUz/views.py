from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Q
from math import log2, pow
from django.forms.models import inlineformset_factory


from .forms import MatchForm, SetsForm, MatchFormFullPP, MatchFormFullP, TourneyGroupPlayerForm,PlayerRankForm, TourneyGroupForm, SelectTourneyGroupForm
from .models import Question, Choice, News, Match, Set, Tourney, Tourney_Group, Tourney_Group_Player, Myimage,Player,Player_Rank
from .tables import RankTable
from django_tables2 import RequestConfig

from django.db import connection



def my_custom_sql(tid):
    s= '''SELECT  pe.last_name ||' '|| pe.first_name ,  pl.id ,pr.rank_in_tourney, pr.delta_rahk
    FROM TennisUz_tourney_group_player gp
    INNER JOIN TennisUz_tourney_group tg on  gp.tourney_group_id = tg.id   
    INNER JOIN TennisUz_player pl on  gp.player_id = pl.id      
    INNER JOIN TennisUz_person pe on  pl.person_id = pe.id  
    Left JOIN  TennisUz_player_rank pr   on (pr.player_id = pl.id) and (pr.tourney_id = tg.tourney_id)
    WHERE tg.tourney_id = {tid}
    Order by 3,1
       '''.format(tid = tid)
    with connection.cursor() as cursor:
        cursor.execute(s)
        row = cursor.fetchall()

    return row


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
    tourney_players = Tourney_Group_Player.objects.filter(tourney_group__tourney_id=tid).order_by('player')
    tourney_players_2 = my_custom_sql(tid)
    context = {
        'tourney': tourney,
        'last_resusts_list':last_resusts_list,
        'tourney_players':tourney_players,
        'tourney_players_2':tourney_players_2
    }
    return  render(request,'tourney/detail.html',context)

def get_table_group_by_id(gid):
    tourney_group = get_object_or_404(Tourney_Group, pk=gid)
    # n_players =tourney_group.n_players
    players = Tourney_Group_Player.objects.filter(tourney_group=gid).order_by('nn')
    # ToDo find place every playr
    ttt = []
    for p1 in players:
        ttt.append([p1])
        # p1.rank = 12
        for p2 in players:
            mps = Match.objects.filter(tourney_group_id=gid, player1_id=p1.player_id, player2_id=p2.player_id)
            if len(mps)>0:
                mp = mps[0]
                v = mp.parse_score()
                ttt.append([1 if v[1]>v[2] else 0,v[1]-v[2], v[3]-v[4]])
            else:
                ttt.append([0,0,0])

    ttt.sort#(key = lambda row: ( row[1], row[2]),reverse=True)


    #

    n_players = len(players)
    tg = []
    i = 1
    y = [tourney_group.name,'Гравці']
    for k in range(n_players):
        y.append(str(k+1))
    y.append('Ігри')
    y.append('Бали')
    y.append('Сети')
    y.append('Гейми')
    # y.append('Місце')
    tg.append(y)
    #get group rank players



    for p in players.order_by('rank'):
        p.rank = 2;
        y = [str(i), str(p.player)+'/'+str(p.player2) if p.player2 else str(p.player)]
        matches, points,sets1,sets2, games1,games2 = 0,0,0,0,0,0
        for p1 in players.order_by('rank'):
            if p1.id == p.id:
                y.append('x')
            else:
                m1 = Match.objects.filter(tourney_group_id=gid, player1_id= p.player_id, player2_id=p1.player_id)
                m2 = Match.objects.filter(tourney_group_id=gid, player1_id=p1.player_id, player2_id= p.player_id)
                if len(m1)>0:
                    m=m1[0]
                    matches+=1
                    if m.s1()>m.s2():
                        points +=1
                    elif (m.withdrawal and m.winner==1):
                        points += 1

                    sets1 += m.s1()
                    sets2 += m.s2()
                    games1 += m.g1()
                    games2 += m.g2()
                    y.append(m.score1())
                elif len(m2)>0:
                    m = m2[0]
                    matches += 1
                    if m.s1() < m.s2():
                        points += 1
                    elif (m.withdrawal and m.winner == 2):
                        points += 1
                    sets1 += m.s2()
                    sets2 += m.s1()
                    games1 += m.g2()
                    games2 += m.g1()
                    y.append(m.score2())
                else:
                    y.append('-')
        y.append(str(matches))
        y.append(str(points))
        y.append(str(sets1) + '-' +str(sets2))
        y.append(str(games1) + '-' + str(games2))
        # y.append(str(p.rank))

        i=i+1
        tg.append(y)
        # tg1 = tg.sort(key = lambda row: (row[-3],row[-2]),reverse=True)
    return tg#.sort(key = lambda row: row[-3],reverse=True)




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
            r['first_round'] = (i == (n_round - 1))
            r['pk'] = 0
            r['nn'] = 0
            r['perc'] = perc
            r['i'] = n_round - i
            r['i'] = 1
            if len(m1) > 0:
                m = m1[0]
                r['nn'] = m.group_id
                r['pk'] = m.pk
                r['p'] = m.pp()
                r['r'] = m.score1()
                r['p1'] = m.pplayer1()
                r['p2'] = m.pplayer2()
                r['pp'] =  m.is_pp()
                r['is_match'] = True
                y.append(r)
            else:
                r['p'] =' '
                r['r'] = ' '
                r['p1'] = ' '
                r['p2'] = ' '
                r['pp'] = False
                r['is_match'] = False
                y.append(r)
        perc = perc // 2
        pf.insert(0,y)
    return pf

def sort_gpoup_table_by_results(tb):
    tb.sort(key = lambda row: row[-3],reverse=True)
    n = len(tb)
    for i in range(n-1):
        tt = [x  for x in tb if x[-3] == tb[i][-3]]
        if len(tt) == 2:
            pass
        if len(tt) > 2:
            pass

        pass
    return tb


def tourney_group_detail(request,tid, gid):
    tourney_group = get_object_or_404(Tourney_Group, pk=gid)
    tourney = get_object_or_404(Tourney, pk=tid)
    tg = get_table_group_by_id(gid)
    pf = get_pf_by_id(gid)
    tb =tg[1:]
    tourney_players = Tourney_Group_Player.objects.filter(tourney_group_id=gid).order_by('player')

    last_resusts_list = Match.objects.filter(tourney_group_id=gid).order_by('-dt')
    context = {
        'pf':pf,
        'tourney':tourney,
        'tourney_group_head': tg[:1],
        'tourney_group_body':tb,
        'tourney_group':tourney_group,
        'last_resusts_list':last_resusts_list,
        'tb':tb,
        'tourney_players' : tourney_players,

    }
    return  render(request,'tourney/group_detail.html',context)

def generate_matches(request,tid, gid):
    tourney_group = get_object_or_404(Tourney_Group, pk=gid)
    is_pf = tourney_group.play_off
    tourney = get_object_or_404(Tourney, pk=tid)
    players = Tourney_Group_Player.objects.filter(tourney_group=gid).order_by('nn')
    n_players = len(players)
    nn = 0
    if not is_pf:
        ppp = set()
        for p1 in players:
            for p2 in players:
                if (not (p2 in ppp)) and (p1 != p2):
                    tm = Match(tourney_group_id=gid,
                           game_type_id=1,
                           is_official=True,
                           player1_id=p1.player_id,
                           player3_id=p1.player2_id,
                           player2_id=p2.player_id,
                           player4_id=p2.player2_id,)
                    if p1.player2 or p2.player2: tm.game_type_id =2
                    tm.dt = tourney.dt
                    tm.group_id = nn
                    nn = nn+1
                    tm.save()
            ppp.add(p1)
    else:
        for i in range(1, tourney_group.n_players):
            m = Match.objects.filter(tourney_group_id=gid, group_id=i)
            if len(m)==0:
                tm = Match(tourney_group_id=gid,
                       game_type_id=tourney.game_type_id,
                       is_official=True,
                       group_id=i)
                tm.dt = tourney.dt
                tm.save()

    last_resusts_list = Match.objects.filter(tourney_group_id=gid).order_by('-dt')
    return HttpResponseRedirect(reverse('tourney_group_detail', args=(tid,gid)))

def fill_1pf(request,tid, gid, nn):
    current_Match = Match.objects.filter(tourney_group_id=gid,group_id=nn)[0]
    tourney_group = get_object_or_404(Tourney_Group, pk=gid)
    is_pf = tourney_group.play_off
    tourney = get_object_or_404(Tourney, pk=tid)
    para = (tourney.game_type_id ==2)
    n_players = tourney_group.n_players
    first_raund = (nn>=n_players/2)
    if not first_raund:
        ms1 = Match.objects.filter(tourney_group_id=gid, group_id=nn*2)
        if len(ms1)>0:
            m1 = ms1[0]
            if m1.winner()>0:
                if m1.winner() == 1:
                    current_Match.player1_id = m1.player1_id
                    if para:
                        current_Match.player3_id = m1.player3_id
                else:
                    if m1.winner() ==2:
                        current_Match.player1_id = m1.player2_id
                        if para:
                            current_Match.player3_id = m1.player4_id
        ms2 = Match.objects.filter(tourney_group_id=gid, group_id=nn*2+1)
        if len(ms2)>0:
            m2 = ms2[0]
            if m2.winner() == 1:
                current_Match.player2_id = m2.player1_id
                if para:
                    current_Match.player4_id = m2.player3_id
            else:
                if m2.winner() == 2:
                    current_Match.player2_id = m2.player2_id
                    if para:
                        current_Match.player4_id = m2.player4_id

        current_Match.save()
    else:
        if tourney_group.max_rank>1: # not main
            draws = tourney.draw_counts.replace(' ','')
            draws1 =[0] + [int(i) for i in draws.split(',') if i.isdigit()]+[1000]
            draws1.append(tourney_group.max_rank)
            draws1.sort()

            j = draws1.index(tourney_group.max_rank)
            if j>0:
                target_draws = draws1[j-1] +1
            else:
                target_draws =1

            target_group_list = Tourney_Group.objects.filter(tourney_id=tid, play_off=1,max_rank=target_draws)
            if len(target_group_list)>0:
                target_group_id = target_group_list[0]

            ms1 = Match.objects.filter(tourney_group_id=target_group_id, group_id=nn*2 )
            if len(ms1) > 0:
                m1 = ms1[0]
                if m1.winner() > 0:
                    if m1.winner() == 1:
                        current_Match.player1_id = m1.player2_id
                        if para:
                            current_Match.player3_id = m1.player4_id
                    else:
                        if m1.winner() == 2:
                            current_Match.player1_id = m1.player1_id
                            if para:
                                current_Match.player3_id = m1.player3_id
            ms2 = Match.objects.filter(tourney_group_id=target_group_id, group_id=nn *2+ 1)
            if len(ms2) > 0:
                m2 = ms2[0]
                if m2.winner() == 1:
                    current_Match.player2_id = m2.player2_id
                    if para:
                        current_Match.player4_id = m2.player4_id
                else:
                    if m2.winner() == 2:
                        current_Match.player2_id = m2.player1_id
                        if para:
                            current_Match.player4_id = m2.player3_id

            current_Match.save()
    return HttpResponseRedirect(reverse('tourney_group_detail', args=(tid, gid)))


def tourney_group_players_add(request, tid, gid):
    inst = Tourney_Group_Player()
    ppp = Tourney_Group_Player.objects.filter(tourney_group_id=gid).order_by('-nn')
    if len(ppp)>0:
        nn1 = ppp[0].nn+1
    else:
        nn1 =1
    inst.tourney_group_id = gid;
    inst.nn = nn1
    inst.rank = nn1
    if request.method == 'POST':
        form = TourneyGroupPlayerForm(request.POST, instance=inst)
        if form.is_valid():
            inst.save()
            return HttpResponseRedirect(reverse('tourney_group_detail', args=(tid, gid)))
    else:
        form = TourneyGroupPlayerForm(instance=inst)

    return render(request, 'tourney/group_player.html', {'form': form, 'inst':inst})



def new_match(request):
    form = MatchForm()
    return render(request, 'tourney/match.html', {'form': form})


def match1(request, mid):
    match_inst = get_object_or_404(Match, pk=mid)
    gid = match_inst.tourney_group_id
    tid = match_inst.tourney_group.tourney_id
    form_set = inlineformset_factory(Match,Set,fields=('g1','g2'))
    if request.method == 'POST':
        form = form_set(request.POST, instance=match_inst)
        if form.is_valid():
            match_inst.save()
            return HttpResponseRedirect(reverse('tourney_group_detail', args=(tid, gid)))
    else:
        form = form_set(instance=match_inst)

    return render(request, 'tourney/match.html', {'form': form, 'matchinst':match_inst})

def match(request, mid):
    match_inst = get_object_or_404(Match, pk=mid)
    gid = match_inst.tourney_group_id
    tid = match_inst.tourney_group.tourney_id
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match_inst)
        if form.is_valid():
            match_inst.save()
            return HttpResponseRedirect(reverse('tourney_group_detail', args=(tid, gid)))
    else:
        form = MatchForm(instance=match_inst)

    return render(request, 'tourney/match.html', {'form': form, 'matchinst':match_inst})

def matchp(request, mid):
    match_inst = get_object_or_404(Match, pk=mid)
    gid = match_inst.tourney_group_id
    tid = match_inst.tourney_group.tourney_id
    tourney = get_object_or_404(Tourney, pk=tid)
    if request.method == 'POST':
        if tourney.game_type_id==1:
            form = MatchFormFullP (request.POST, instance=match_inst)
        else:
            form = MatchFormFullPP(request.POST, instance=match_inst)

        if form.is_valid():
            match_inst.save()
            return HttpResponseRedirect(reverse('tourney_group_detail', args=(tid, gid)))
    else:
        if tourney.game_type_id==1:
            form = MatchFormFullP ( instance=match_inst)
        else:
            form = MatchFormFullPP(instance=match_inst)

    return render(request, 'tourney/match.html', {'form': form, 'matchinst':match_inst})

def matchpp(request, mid):
    pass


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

def tourney_rules(request):

    return render(request, 'tourney/rules.html')

def add_players_to_group(request):
    pass

def players(request):
    players_list = Player.objects.all().order_by('person')
    return render(request, 'players/list.html', {'players_list' : players_list})

def player_info(request,pid):
    player = get_object_or_404(Player, pk=pid)
    return render(request, 'players/info.html', {'player': player})

def tourney_player_rank(request,tid,pid):
    inst1 = Player_Rank.objects.filter(tourney_id=tid,player_id=pid)
    tourney = get_object_or_404(Tourney, pk=tid)
    if len(inst1)>0:
        inst = inst1[0]
    else:
        inst = Player_Rank()
        inst.tourney_id = tid
        inst.player_id = pid
        inst.dt = tourney.dt
    if request.method == 'POST':
        form = PlayerRankForm(request.POST, instance=inst)
        if form.is_valid():
            inst.save()
            return HttpResponseRedirect(reverse('tourney_detail', args=(tid,)))
    else:
        form = PlayerRankForm(instance=inst)

    return render(request, 'tourney/playr_rank.html', {'form': form, 'inst':inst})

def tourney_group_add(request,tid):
    inst = Tourney_Group()
    inst.tourney_id = tid

    if request.method == 'POST':
        form = TourneyGroupForm(request.POST, instance=inst)
        if form.is_valid():
            inst.save()
            return HttpResponseRedirect(reverse('tourney_detail', args=(tid,)))
    else:
        form = TourneyGroupForm(instance=inst)

    return render(request, 'tourney/group_add.html', {'form': form, 'inst':inst})

def players_move_to_group(request,tid,pid):
    inst = get_object_or_404(Tourney_Group_Player, pk=pid)
    if request.method == 'POST':
        form = SelectTourneyGroupForm(request.POST,instance=inst, tid=tid )
        if form.is_valid():
            inst.tourney_group = form.cleaned_data['g']
            inst.save()
            return HttpResponseRedirect(reverse('tourney_detail', args=(tid,)))
    else:
        form = SelectTourneyGroupForm(instance=inst,tid=tid)
    return render(request, 'tourney/move_to_group.html', {'form': form, 'inst':inst })

from django.db.models import Count, Avg,Sum

def select_rank():
    s= '''SELECT  pe.last_name ||' '|| pe.first_name ,  pl.id , sum(pr.delta_rahk)
    FROM TennisUz_player_rank pr
    INNER JOIN TennisUz_player pl on  pr.player_id = pl.id
    INNER JOIN TennisUz_person pe on  pl.person_id = pe.id
group by 1,2

    Order by 3 desc,1
       '''
    with connection.cursor() as cursor:
        cursor.execute(s)
        row = cursor.fetchall()

    return row

def ranking(request):
    pr = select_rank()#Player.objects.all().order_by('player')
    table = RankTable(pr)
    table.paginate(page=request.GET.get("page", 1), per_page=32)
    RequestConfig(request).configure(table)
    return render(request,'tourney/ranking.html',{'rank':table, 'pr':pr})