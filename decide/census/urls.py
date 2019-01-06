from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('list/', views.CensuslListView.as_view(), name='census_list'),
    path('list/<int:voting_id>/', views.CensuslByVotingListView.as_view(), name='census_by_voting_list'),
    path('list/votingByDate/', views.VotingByDateListView.as_view(), name='voting_by_date_list'),
    path('list/user/<int:voter_id>/', views.VotingListView.as_view(), name="voting_list"),
    path('list/voting/<int:voting_id>/', views.UserListView.as_view(), name="user_list"),
    path('voter/<int:voter_id>/', views.CensusList.as_view(), name="votings_by_voter")
]
