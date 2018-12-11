from django.urls import path
from . import views
from voting.views import crear_referendum, create_options, home

urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('home', home),
    path('referendum', crear_referendum),
    path('options', create_options)

]