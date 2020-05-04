from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.NewsIndexView.as_view(), name='news_index'),
    path('tourney/', views.tourney_index, name='tourney_index'),
    path('tourney/<int:question_id>', views.tourney_detail, name='tourney_detail'),
    path('tourney/spring2020/', views.tourney_spring2020, name='tourney_spring2020'),
    # path('poll/', views.poll_index, name='poll_index'),
    # path('poll/<int:question_id>/', views.poll_detail, name='poll_detail'),
    # # ex: /polls/5/results/
    # path('poll/<int:question_id>/results/', views.poll_results, name='poll_results'),
    # ex: /polls/5/vote/
    path('poll/', views.PollIndexView.as_view(), name='poll_index'),
    path('poll/<int:pk>/', views.PollDetailView.as_view(), name='poll_detail'),
    path('poll/<int:pk>/results/', views.PollResultsView.as_view(), name='poll_results'),
    path('poll/<int:question_id>/vote/', views.poll_vote, name='poll_vote'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)