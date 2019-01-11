from django.urls import path
from .views import GetUserView, LogoutView, LoginView, Signup, Activate, GetUserByUsernameView
from django.contrib.auth import views
from django .contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('getuserbyusername/', GetUserByUsernameView.as_view()),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('signup/', Signup.as_view()),
    path('activate/<uid>/<token>/', Activate.as_view(), name='activate')

] + staticfiles_urlpatterns()



