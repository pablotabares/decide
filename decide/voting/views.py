import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import render, redirect

from django.http.response import HttpResponse
from .models import Question, QuestionOption, Voting
from .serializers import VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
from voting.forms import QuestionForm, QuestionOptionsForm, someQuestionsOptions, VotingForm2
from django.template import loader


def home(request):
    return render(request, 'masterpage.html', {'title': 'Home', 'content': 'home.html'})


def crear_referendum(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            name_voting = form.cleaned_data['name_voting']
            desc_voting = form.cleaned_data['desc_voting']
            name_auth = form.cleaned_data['name_auth']
            url_auth = form.cleaned_data['url_auth']
            desc_question = form.cleaned_data['desc_question']

            question = Question(desc=desc_question)
            question.save()

            opt_yes = QuestionOption(question=question, option="Yes", number=1)
            opt_no = QuestionOption(question=question, option="No", number=2)
            opt_yes.save()
            opt_no.save()

            questions = [question]

            voting = Voting(name=name_voting, desc=desc_voting)
            voting.save()
            voting.questions.set(questions)

            auth = Auth(name=name_auth, url=url_auth, me=True)
            auth.save()
            voting.auths.add(auth)

            return render(request, 'referendumcreated.html')
    else:
        form = QuestionForm()

    return render(request, 'masterpage.html', {'form': form, 'content': 'referendumform.html',
                                               'title': 'Create a referendum'})


def create_options(request):
    if request.method == "POST":
        print()  # TODO: manejar las entradas
    else:
        form = someQuestionsOptions()

    return render(request, 'masterpage.html', {'form': form, 'content': 'questionForm.html', 'title': 'Create options'})


def create_voting(request):
    if request.method == "POST":
        form = VotingForm2(request.POST)
        if form.is_valid():
            name_voting = form.cleaned_data['name_voting']
            desc_voting = form.cleaned_data['desc_voting']
            is_weighted = form.cleaned_data['is_weighted']

            name_auth = form.cleaned_data['name_auth']
            url_auth = form.cleaned_data['url_auth']

            question_ = form.cleaned_data['questions_']
            voting = Voting(name=name_voting, desc=desc_voting, isWeighted=is_weighted)

            voting.save()
            voting.questions.set(question_)

            auth = Auth(name=name_auth, url=url_auth, me=True)
            auth.save()
            voting.auths.add(auth)

            return render(request, 'votingCreated.html')
    else:
        form = VotingForm2()

    return render(request, 'masterpage.html', {'form': form, 'content': 'votingForm.html', 'title': 'Create a voting'})


class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('id',)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)

        if 'multiple' in request.data:
            for data in ['name', 'desc', 'questions']:
                if not data in request.data:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)

            voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'))
            voting.save()

            for q in request.data.get('questions'):

                question = Question(desc=q['desc'])
                question.save()
                voting.questions.add(question)

                for idx, q_opt in enumerate(q['options']):
                    opt = QuestionOption(question=question, option=q_opt['option'], number=idx)
                    opt.save()

                    if q_opt.get('unlocksQuestions'):

                        for q2 in q_opt['unlocksQuestions']:
                            question = Question(desc=q2['desc'])
                            question.save()
                            opt.unlockquestion.add(question)

                            for idx2, q_opt2 in enumerate(q2['options']):
                                opt = QuestionOption(question=question, option=q_opt2['option'], number=idx2)
                                opt.save()


        else:

            for data in ['name', 'desc', 'question', 'question_opt']:
                if not data in request.data:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)

            question = Question(desc=request.data.get('question'))
            question.save()

            for idx, q_opt in enumerate(request.data.get('question_opt')):
                opt = QuestionOption(question=question, option=q_opt, number=idx)
                opt.save()
            voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'))
            voting.save()
            voting.questions.add(question)

            auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                                 defaults={'me': True, 'name': 'test auth'})
            auth.save()
            voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)


class VotingUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_id, *args, **kwars):
        action = request.data.get('action')
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(Voting, pk=voting_id)
        msg = ''
        st = status.HTTP_200_OK
        if action == 'start':
            if voting.start_date:
                msg = 'Voting already started'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = 'Voting started'
        elif action == 'stop':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = 'Voting already stopped'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = 'Voting stopped'
        elif action == 'tally':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = 'Voting is not stopped'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = 'Voting already tallied'
                st = status.HTTP_400_BAD_REQUEST
            else:
                res = voting.tally_votes(request.auth.key)
                if res != 'Voting tallied':
                    msg = res
                    st = status.HTTP_400_BAD_REQUEST
                else:
                    msg = 'Voting tallied'
        else:
            msg = 'Action not found, try with start, stop or tally'
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)


class VotingReferendumView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('id',)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'question', 'question_opt']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = Question(desc=request.data.get('question'))
        question.save()

        opt_yes = QuestionOption(question=question, option="Yes", number=1)
        opt_no = QuestionOption(question=question, option="No", number=2)
        opt_yes.save()
        opt_no.save()

        voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'))
        voting.save()
        voting.questions.add(question)

        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                             defaults={'me': True, 'name': 'test auth'})
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)
