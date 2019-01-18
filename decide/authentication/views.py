from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .serializers import UserSerializer, AuthCustomTokenSerializer
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator

#Nuevo
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, Http404, get_object_or_404
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegisterUser
from .serializers import UserSerializer
from .tokens import activation_token
from django.contrib.auth.models import User
from django.conf import settings


class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class LoginView(APIView):
    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)



        return Response({'token': token.key})

    def get_ip_from_request(self, request):

        if request.META.get('HTTP_CLIENT_IP'):
            ip = request.META.get('HTTP_CLIENT_IP')
        elif request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get('HTTP_X_FORWARDED_FOR')
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip


class PasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'registration/password_reset_form.html',
    email_template_name = 'registration/password_reset_email.html',
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = 'done'
    token_generator = default_token_generator


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    token_generator = default_token_generator


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    form_class = SetPasswordForm


class Signup(APIView):
    def post(self, request):
        form = RegisterUser(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = False
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            instance = User.objects.create_user(username, email=email, password=password)
            instance.save()
            site = get_current_site(request)
            mail_subject = "Confirmation message for Decide"
            message = render_to_string('acc_active_email.html', {
                "user": instance,
                'domain': site.domain,
                'uid': instance.id,
                'token': activation_token.make_token(instance)
            })
            to_email = form.cleaned_data.get('email')
            to_list = [to_email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
            return HttpResponse("<h1>Thanks for your registration. A confirmation link was sent to your email</h1>")
        return render(request, 'signup.html', {"form": form})


class Activate(APIView):
    def post(self, request, uid, token):
        try:
            user = get_object_or_404(User, pk=uid)
        except:
            raise Http404("No user found")
        if user is not None and activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("<h1>Account is activated. Now you can <a href='/login'>login</a></h1>")
        else:
            return HttpResponse("<h3>Invalid activation link</h3>")