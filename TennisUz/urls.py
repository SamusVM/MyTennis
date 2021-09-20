from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.NewsIndexView.as_view(), name='news_index'),
    path('results/last/', views.last_results, name='last_results_index'),
    path('tourney/', views.tourney_index, name='tourney_index'),
    path('tourney/rules', views.tourney_rules, name='tourney_rules'),
    path('tourney/ranking', views.ranking, name='ranking'),

    path('tourney/<int:tid>/group/<int:gid>', views.tourney_group_detail, name='tourney_group_detail'),
    path('tourney/<int:tid>/group/<int:gid>/generate_matches', views.generate_matches, name='generate_matches'),
    path('tourney/<int:tid>/group/<int:gid>/players/add', views.tourney_group_players_add, name='tourney_group_players_add'),

    path('tourney/<int:tid>', views.tourney_detail, name='tourney_detail'),
    path('tourney/<int:tid>/player/<int:pid>/rank', views.tourney_player_rank, name='tourney_player_rank'),
    path('tourney/<int:tid>/player/<int:pid>/move_to_group', views.players_move_to_group, name='players_move_to_group'),

    path('tourney/<int:tid>/group_add', views.tourney_group_add, name='tourney_group_add'),

    path('players/<int:pid>', views.player_info, name='player_info'),
    path('players/list', views.players, name='players'),
    path('match/new', views.new_match, name='new_match'),
    path('match/<int:mid>', views.match, name='match'),
    path('matchp/<int:mid>', views.matchp, name='matchp'),
    path('matchpp/<int:mid>', views.matchpp, name='matchpp'),
    path('tourney/<int:tid>/group/<int:gid>/fill_pf/<int:nn>', views.fill_1pf, name='fill_1pf'),
    path('tourney/spring2020/', views.tourney_spring2020, name='tourney_spring2020'),

    path('poll/', views.PollIndexView.as_view(), name='poll_index'),
    path('poll/<int:pk>/', views.PollDetailView.as_view(), name='poll_detail'),
    path('poll/<int:pk>/results/', views.PollResultsView.as_view(), name='poll_results'),
    path('poll/<int:question_id>/vote/', views.poll_vote, name='poll_vote'),
    path('foto/', views.foto_index, name='foto_index'),
    path('foto/<int:pk>/', views.foto_detail, name='foto_detail'),
]
              # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)