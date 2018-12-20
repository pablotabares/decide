from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('list', views.CensuslListView.as_view(), name='census_list'),
    path('list/<int:voting_id>/', views.CensuslByVotingListView.as_view(), name='census_by_voting_list'),
]
