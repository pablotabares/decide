from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods
from census.models import Census
from voting.models import Voting
from rest_framework.authtoken.models import Token
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
from .models import Visualizer
from voting.models import Voting
from voting.serializers import VotingSerializer

class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        admin_id = User.objects.filter(is_staff='t').first().id
        try:
            tk = Token.objects.filter(user_id=admin_id)[0].key
            r = mods.get('voting', params={'id': vid})
            c = mods.get('census', params={'voting_id': vid}, HTTP_AUTHORIZATION='Token ' + tk)
            #Investigar otra forma de pasar Token
            context['voting'] = r[0]
            context['census'] = c
        except:
            raise Http404

        return context



class VisualizerJSON(generics.ListAPIView):
    serializer_class = VisualizerSerializer
    model = serializer_class.Meta.model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        admin_id = User.objects.filter(is_staff='t').first().id
        try:
            tk = Token.objects.filter(user_id=admin_id)[0].key
            r = mods.get('voting', params={'id': vid})
            c = mods.get('census', params={'voting_id': vid}, HTTP_AUTHORIZATION='Token ' + tk)
            #Investigar otra forma de pasar Token
            context['voting'] = r[0]
            context['census'] = c
        except:
            raise Http404

        return context
