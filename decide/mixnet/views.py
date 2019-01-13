from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden, HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MixnetSerializer
from .models import Auth, Mixnet, Key
from base.serializers import KeySerializer, AuthSerializer
from mixnet.populate import createQuestion, createAnswers, createVotation, createUsers
from base import mods
from mixnet.forms import LoginForm
from django.views.generic import TemplateView


class MixnetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mixnets to be viewed or edited.
    """
    queryset = Mixnet.objects.all()
    serializer_class = MixnetSerializer

    def create(self, request):
        """
        This create a new mixnet and public key

         * auths: [ {"name": str, "url": str} ]
         * voting: id
         * position: int / nullable
         * key: { "p": int, "g": int } / nullable
        """

        auths = request.data.get("auths")
        voting = request.data.get("voting")
        key = request.data.get("key", {"p": 0, "g": 0})
        position = request.data.get("position", 0)
        p, g = int(key["p"]), int(key["g"])

        dbauths = []
        for auth in auths:
            isme = auth["url"] == settings.BASEURL
            a, _ = Auth.objects.get_or_create(name=auth["name"],
                                              url=auth["url"],
                                              me=isme)
            dbauths.append(a)

        mn = Mixnet(voting_id=voting, auth_position=position)
        mn.save()

        for a in dbauths:
            mn.auths.add(a)

        mn.gen_key(p, g)

        data = { "key": { "p": mn.key.p, "g": mn.key.g } }
        # chained call to the next auth to gen the key
        resp = mn.chain_call("/", data)
        if resp:
            y = (resp["y"] * mn.key.y) % mn.key.p
        else:
            y = mn.key.y

        pubkey = Key(p=mn.key.p, g=mn.key.g, y=y)
        pubkey.save()
        mn.pubkey = pubkey
        mn.save()

        return  Response(KeySerializer(pubkey, many=False).data)


class Shuffle(APIView):

    def post(self, request, voting_id):
        """
         * voting_id: id
         * msgs: [ [int, int] ]
         * pk: { "p": int, "g": int, "y": int } / nullable
         * position: int / nullable
        """

        position = request.data.get("position", 0)
        mn = get_object_or_404(Mixnet, voting_id=voting_id, auth_position=position)

        msgs = request.data.get("msgs", [])
        pk = request.data.get("pk", None)
        if pk:
            p, g, y = pk["p"], pk["g"], pk["y"]
        else:
            p, g, y = mn.key.p, mn.key.g, mn.key.y

        msgs = mn.shuffle(msgs, (p, g, y))

        data = {
            "msgs": msgs,
            "pk": { "p": p, "g": g, "y": y },
        }
        # chained call to the next auth to gen the key
        resp = mn.chain_call("/shuffle/{}/".format(voting_id), data)
        if resp:
            msgs = resp

        return  Response(msgs)


class Decrypt(APIView):

    def post(self, request, voting_id):
        """
         * voting_id: id
         * msgs: [ [int, int] ]
         * pk: { "p": int, "g": int, "y": int } / nullable
         * position: int / nullable
        """

        position = request.data.get("position", 0)
        mn = get_object_or_404(Mixnet, voting_id=voting_id, auth_position=position)

        msgs = request.data.get("msgs", [])
        pk = request.data.get("pk", None)
        if pk:
            p, g, y = pk["p"], pk["g"], pk["y"]
        else:
            p, g, y = mn.key.p, mn.key.g, mn.key.y

        next_auths = mn.next_auths()
        last = next_auths.count() == 0

        # useful for tests only, to override the last value
        last = request.data.get("force-last", last)

        msgs = mn.decrypt(msgs, (p, g, y), last=last)

        data = {
            "msgs": msgs,
            "pk": { "p": p, "g": g, "y": y },
        }
        # chained call to the next auth to gen the key
        resp = mn.chain_call("/decrypt/{}/".format(voting_id), data)
        if resp:
            msgs = resp

        return  Response(msgs)

class Populate(TemplateView):
    # HTML template to be used
    template_name = 'mixnet_populate.html'
    
    # Data necessary for the webpage to display
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question = createQuestion()
        answers = createAnswers(question)
        votation = createVotation(question)
        users = createUsers(votation)

        context['users'] = users
        context['answers'] = answers
        context['votation'] = votation
        context['question'] = question
        context['mixnet_url'] = settings.APIS.get('mixnet', settings.BASEURL)

        return context

    def get(self, request):
        form = LoginForm()
        return render(request, 'populate_login.html', {'form': form})

    def post(self, request):
        # Extracts data from form
        form = LoginForm(request.POST)
        data = {
            "username": form.data["username"],
            "password": form.data["password"],
        }
        
        # Logs in
        token = mods.post('authentication/login', baseurl=settings.APIS.get('authentication', settings.BASEURL), json=data)
        
        # Tries to get user data
        try:
            user = mods.post('authentication/getuser', baseurl=settings.APIS.get('authentication', settings.BASEURL), json={"token": token["token"]})
            # If it's not an admin
            if(not user["is_staff"]):
                return render(request, 'populate_login.html', {'form': form, "error": "Only administrator can populate the database"})
            # If it's an admin
            else:
                return render(request, "mixnet_populate.html", self.get_context_data())
        except KeyError as k:
            # If incorrect user/pass
            return render(request, 'populate_login.html', {'form': form, "error": "Incorrect username or password"})
        except Exception as e:
            # If unknown error
            print(e)
            return HttpResponse("Unexpected server error")
        return HttpResponse("Unexpected server error")
