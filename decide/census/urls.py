from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('list/', views.CensuslListView.as_view(), name='census_list'),
    path('list/<int:voting_id>/', views.CensuslByVotingListView.as_view(), name='census_by_voting_list'),
    path('list/user/<int:voter_id>/votingFilter/', views.VotingFilterListView.as_view(), name='voting_filter_list'),
    path('list/user/<int:voter_id>/<str:orden>/', views.orderingVotingByListView.as_view(), name='ordering_by_list'),
    path('list/user/<int:voter_id>/', views.VotingListView.as_view(), name="voting_list"),
    path('list/voting/<int:voting_id>/', views.UserListView.as_view(), name="user_list"),
    path('voter/<int:voter_id>/', views.CensusList.as_view(), name="votings_by_voter"),
    path('ldap/', views.LDAP.as_view(), name="ldap"),
]
