from django.db.utils import IntegrityError
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from django.views.generic.list import ListView
from rest_framework.renderers import JSONRenderer
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from .models import Census
from voting.models import Voting
from voting.serializers import VotingSerializer

class VotingListView(ListView):
    model = Voting
    template_name = "voting_list.html"
    voter_id = 0

    def get(self, request, *args, **kwargs):
        self.voter_id = kwargs.get('voter_id')
        return ListView.get(self, request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        ids = Census.objects.filter(voter_id=self.voter_id).values('voting_id')
        object_list = Voting.objects.filter(pk__in=ids)
        return super().get_context_data(object_list=object_list, **kwargs)

class UserListView(ListView):
    model = User
    template_name = "user_list.html"
    voting_id = 0

    def get(self, request, *args, **kwargs):
        self.voting_id = kwargs.get('voting_id')
        return ListView.get(self, request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        ids = Census.objects.filter(voting_id=self.voting_id).values('voter_id')
        object_list = User.objects.filter(pk__in=ids)
        return super().get_context_data(object_list=object_list, **kwargs)


class CensuslListView(ListView):
    model = Census
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ids = Census.objects.values('voting_id').distinct()
        userIds = Census.objects.values('voter_id').distinct()
        context['userList'] = User.objects.all().filter(pk__in=userIds)
        context['votingList'] = Voting.objects.all().filter(pk__in=ids)
        return context

class VotingByDateListView(ListView):
    model = Census
    template_name = "list.html"
    startDate = None
    endDate = None
    voting = None
    ids = None

    def post(self, request, *args, **kwargs): #We took the data of the form
        form = self.get_form()
        if form.is_valid():
            datos = form.cleaned_data
            try:
                self.voting = Voting.objects.filter(start_date__gte=datos['startDate']).filter(end_date__lte=datos['endDate'])
            except ObjectDoesNotExist as n:
                return redirect('census_list')       
        return ListView.get(self, request, *args,**kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for vote in self.voting:
            ids = ids.append(Census.objects.filter(voting_id=vote.get('id').values('voter_id')))
        context['object_list'] = User.objects.all().filter(pk__in=ids)
        context['voting'] = self.voting
        print(kwargs)
        return context
        
class CensuslByVotingListView(ListView):
    model = Census
    template_name = "dashboard.html"
    votingId = 0
    voting = None
    
    def get(self, request, *args, **kwargs):
        self.votingId = kwargs.get('voting_id')
        try:
            self.voting = Voting.objects.get(pk=self.votingId)
        except ObjectDoesNotExist as n:
            return redirect('census_list')
        return ListView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ids = Census.objects.filter(voting_id=self.votingId).values('voter_id')
        context['object_list'] = User.objects.all().filter(pk__in=ids)
        context['voting'] = self.voting
        print(kwargs)
        return context


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')

class CensusList(generics.ListAPIView):
    serializer_class = VotingSerializer
    model = serializer_class.Meta.model
    
    def get_queryset(self):
        voter_id = self.kwargs['voter_id']
        queryset = self.model.objects.filter(pk__in=Census.objects.filter(voter_id=voter_id).values('voting_id'))
        return queryset