from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.NewsIndexView.as_view(), name='news_index'),
    path('results/last/', views.last_results, name='last_results_index'),
    path('tourney/', views.tourney_index, name='tourney_index'),
    path('tourney/<int:tid>/group/<int:gid>', views.tourney_group_detail, name='tourney_group_detail'),
    path('tourney/<int:tid>', views.tourney_detail, name='tourney_detail'),
    path('tourney/spring2020/', views.tourney_spring2020, name='tourney_spring2020'),
    path('poll/', views.PollIndexView.as_view(), name='poll_index'),
    path('poll/<int:pk>/', views.PollDetailView.as_view(), name='poll_detail'),
    path('poll/<int:pk>/results/', views.PollResultsView.as_view(), name='poll_results'),
    path('poll/<int:question_id>/vote/', views.poll_vote, name='poll_vote'),

]
              # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)