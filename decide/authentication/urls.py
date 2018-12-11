from django.urls import path

from .views import GetUserView, LogoutView, LoginView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
]
