from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods
from census.models import Census
from voting.models import Voting

class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        try:
            r = mods.get('voting', params={'id': vid})
            c = mods.get('census', params={'voting_id': vid}, HTTP_AUTHORIZATION='Token 401d04798f526bb074e51b15fa5a278d933b4108') 
            #Investigar otra forma de pasar Token
            context['voting'] = r[0]
            context['census'] = c
            #print(context)
        except:
            raise Http404

        return context

