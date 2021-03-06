from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('poll/', views.poll_index, name='poll_index'),
    # path('poll/<int:question_id>/', views.poll_detail, name='poll_detail'),
    # # ex: /polls/5/results/
    # path('poll/<int:question_id>/results/', views.poll_results, name='poll_results'),
    # ex: /polls/5/vote/
    path('poll/', views.PollIndexView.as_view(), name='poll_index'),
    path('poll/<int:pk>/', views.PollDetailView.as_view(), name='poll_detail'),
    path('poll/<int:pk>/results/', views.PollResultsView.as_view(), name='poll_results'),
    path('poll/<int:question_id>/vote/', views.poll_vote, name='poll_vote'),

]