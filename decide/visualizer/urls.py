from django.urls import path
from .views import VisualizerView
from .views import VisualizerJSON


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    #path('json/<int:voting_id>/', VisualizerJSON.as_view()),
]
