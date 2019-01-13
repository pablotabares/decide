from Crypto.Util.number import inverse
from django.views import View

from django.conf import settings

import hashlib
from mixnet.zkp_form import ZKPForm
from mixnet.mixcrypt import rand

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden, HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MixnetSerializer
from .models import Auth, Mixnet, Key, ConnectionStatus
from base.serializers import KeySerializer, AuthSerializer
from mixnet.populate import createQuestion, createAnswers, createVotation, createUsers
from base import mods
from mixnet.forms import LoginForm
from django.views.generic import TemplateView

from django.shortcuts import render_to_response

from mixnet.control_panel_utils import pingAuths, mixnetStatus, updateConnections



"""
This class defines a series of related views, with each view specified by a function.
"""

class MixnetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mixnets to be viewed or edited.
    """
    queryset = Mixnet.objects.all()
    serializer_class = MixnetSerializer

    def create(self, request):
        """
        Creates a new mixnet and public key. A mixnet is a series of authorities and certain common properties.
         * auths: [ {"name": str, "url": str} ]
         * voting: id
         * position: int / nullable
         * key: { "p": int, "g": int } / nullable
        """

        try:
            # Retrieves the token from the request
            token = request.data.get("token")
            # Asks the auth module for user info
            response = mods.post('authentication', entry_point="/getuser/", json={"token": token},response=True)
            # Returns a negative response if the user is not an administrator
            if(not response.json()["is_staff"]):
                return HttpResponseForbidden("Forbidden")
        except:
            return HttpResponseForbidden("Forbidden")
        
        # Authorities: different authorities in charge of shuffling and decrypting. Can be in the same system or not
        auths = request.data.get("auths")

        # Voting the mixnet is assigned to, specified by an ID
        voting = request.data.get("voting")

        # Information for creating a public key
        key = request.data.get("key", {"p": 0, "g": 0})

        # Position of the "self" authority in the chain
        position = request.data.get("position", 0)

        # Extracts key data from request
        p, g = int(key["p"]), int(key["g"])

        # Gets, or creates if not created, authorities from the database based on request info
        dbauths = []
        for auth in auths:
            # If the URL of the authority is the same as the URL of the server, it is a local authority and gets special treatment
            isme = auth["url"] == settings.BASEURL
            # Checks if an authority with that name and URL exists and creates it if not
            a, _ = Auth.objects.get_or_create(name=auth["name"],
                                              url=auth["url"],
                                              me=isme)
            dbauths.append(a)

        # Creates and saves the mixnet object with the voting and position. Keys and authority are added later
        mn = Mixnet(voting_id=voting, auth_position=position)
        mn.save()

        # Adds authorities to the newly saved mixnet object
        for a in dbauths:
            mn.auths.add(a)

        # Generates local key part using specified key parameters
        mn.gen_key(p, g)

        # Encodes the key data
        data = { "key": { "p": mn.key.p, "g": mn.key.g } }

        # Makes a chain call to the next authorities to generate the key
        resp = mn.chain_call("/", data)

        # If the call is answered, makes the key with the information attained
        if resp:
            y = (resp["y"] * mn.key.y) % mn.key.p
        # If the call is not answered, that means there is only one authority and does not need to make a multiple-authority key
        else:
            y = mn.key.y

        # Creates and saves the public key object
        pubkey = Key(p=mn.key.p, g=mn.key.g, y=y)
        pubkey.save()

        # Associates the public key with this mixnet
        mn.pubkey = pubkey
        mn.save()

        # Returns the public key to be used to cypher the votes
        return  Response(KeySerializer(pubkey, many=False).data)


# Encrypts and shuffles messages
# The first authority calls the same function for the second, and so on and so forth
class Shuffle(APIView):

    def post(self, request, voting_id):
        """
         * voting_id: id
         * msgs: [ [int, int] ]
         * pk: { "p": int, "g": int, "y": int } / nullable
         * position: int / nullable
        """   
        try:
            # Retrieves the token from the request
            token = request.data.get("token")
            # Asks the auth module for user info
            response = mods.post('authentication', entry_point="/getuser/", json={"token": token},response=True)
            # Returns a negative response if the user is not an administrator
            if(not response.json()["is_staff"]):
                return HttpResponseForbidden("Forbidden")
        except:
            return HttpResponseForbidden("Forbidden")

        # Attempts to get the position of this authority in the chain call; if it's not there, this is the first auth and thus
        # it must be zero.
        position = request.data.get("position", 0)
        mn = get_object_or_404(
            Mixnet, voting_id=voting_id, auth_position=position)

        # Retrieves the vote and public key info
        msgs = request.data.get("msgs", [])
        pk = request.data.get("pk", None)

        # If the public key was not specified, retrieves it from the database
        if pk:
            p, g, y = pk["p"], pk["g"], pk["y"]
        else:
            p, g, y = mn.key.p, mn.key.g, mn.key.y

        # Shuffles and encrypts the messages
        msgs = mn.shuffle(msgs, (p, g, y))

        # Prepares the shuffled and encrypted messages
        data = {
            "msgs": msgs,
            "pk": {"p": p, "g": g, "y": y},
        }

        # chained call to the next auth to gen the key
        # Calls the next authority to shuffle, if it exists
        resp = mn.chain_call("/shuffle/{}/".format(voting_id), data)

        # If this isn't the last authority, returns the message from the next authority
        # Otherwise, just returns the messages it has itself shuffled
        if resp:
            msgs = resp

        return Response(msgs)


class Decrypt(APIView):

    def post(self, request, voting_id):
        """
         * voting_id: id
         * msgs: [ [int, int] ]
         * pk: { "p": int, "g": int, "y": int } / nullable
         * position: int / nullable
        """
        try:
            # Retrieves the token from the request
            token = request.data.get("token")
            # Asks the auth module for user info
            response = mods.post('authentication', entry_point="/getuser/", json={"token": token},response=True)
            # Returns a negative response if the user is not an administrator
            if(not response.json()["is_staff"]):
                return HttpResponseForbidden("Forbidden")
        except:
            return HttpResponseForbidden("Forbidden")

        # Attempts to get the position of this authority in the chain call; if it's not there, this is the first auth and thus
        # it must be zero.
        position = request.data.get("position", 0)
        mn = get_object_or_404(
            Mixnet, voting_id=voting_id, auth_position=position)

	    # Retrieves the encrypted votes and public key info
        msgs = request.data.get("msgs", [])
        pk = request.data.get("pk", None)

 	    # If the public key was not specified, retrieves it from the database
        if pk:
            p, g, y = pk["p"], pk["g"], pk["y"]
        else:
            p, g, y = mn.key.p, mn.key.g, mn.key.y

	    # Retrieves the next authority in the chain
        next_auths = mn.next_auths()
	    # Checks whether or not this is the last authority TODO I think
        last = next_auths.count() == 0

        # useful for tests only, to override the last value
        last = request.data.get("force-last", last)

	    # Decrypts the votes
        msgs = mn.decrypt(msgs, (p, g, y), last=last)

	    # Prepares the partially disencrypted votes
        data = {
            "msgs": msgs,
            "pk": {"p": p, "g": g, "y": y},
        }

        # chained call to the next auth to gen the key
	    # Calls the next authority to finish the decryption
        resp = mn.chain_call("/decrypt/{}/".format(voting_id), data)

	    # If this is the last authority, the message is decrypted; otherwise, get the result from the next authority
        if resp:
            msgs = resp

        return Response(msgs)


def fs_form(request):
    if request.method == 'POST':
        form = ZKPForm(request.POST)
        if form.is_valid():

            secret = form.cleaned_data['secret']
            prime = int(form.cleaned_data['prime'])
            hash_secret = int(hashlib.md5(
                secret.encode()).hexdigest()[:8], 16) % prime
            random1 = form.cleaned_data['r1']
            random2 = form.cleaned_data['r2']
            g = int(pow(rand(prime), 2, prime))
            # g^x mod p
            y = pow(g, hash_secret, prime)
            # g^v mod p
            t = pow(g, random1, prime)
            # r
            r = (random1 - random2 * hash_secret)
            if (r < 0):
                res = (inverse(pow(g, -r, prime), prime)
                       * pow(y, random2, prime)) % prime
            else:
                res = (pow(g, r, prime) * pow(y, random2, prime)) % prime
            boolean = t == res
            if (t == res):
                b = 'Alice has proven she knows the secret'
            else:
                b = 'Alice has not proven she knows the secret'
            objects = {'secret': secret, 'prime': prime, 'hash_secret': hash_secret,
                       'random1': random1, 'random2': random2,
                       'g': g, 'y': y, 't': t, 'r': r, 'res': res, 'b': b}
            return render_to_response('result.html', context=objects)
    else:
        form = ZKPForm()
    return render(request, 'zkp.html', {'form': form})


class Result(View):
    def post(self, request, *args, **kwargs):

        return render(request, 'result.html', context={})
        

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

		

# Class that defines the workings of the control panel
class ControlPanel(TemplateView):
    # HTML template to be used
    template_name = 'mixnet_control_panel.html'
	
	# Data necessary for the webpage to display
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
	
        # Retrieve the list of authorities and their ping
        auths = pingAuths()

        # Retrieve the list of mixnets and their status
        mixnets = mixnetStatus()

        # Retrieve the last connections of the authorities
        auth_status = {}
        for auth in auths:
            auth_status[auth] = ConnectionStatus.objects.all().order_by('-date').filter(auth=auth)
        
        context['auths'] = auths
        context['mixnets'] = mixnets
        context['auth_status'] = auth_status
        context['mixnet_url'] = settings.APIS.get('mixnet', settings.BASEURL)

		return context
		
		
	def get(self, request):
        form = LoginForm()
        return render(request, 'login_mixnet.html', {'form': form})

		
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
                return render(request, 'login_mixnet.html', {'form': form, "error": "You are not an admin. Begone!"})
            # If it's an admin
            else:
                return render(request, "mixnet_control_panel.html", self.get_context_data())
        except KeyError as k:
            # If incorrect user/pass
            return render(request, 'login_mixnet.html', {'form': form, "error": "Incorrect username or password"})
        except Exception as e:
            # If unknown error
            print(e)
            return HttpResponse("Unexpected server error")
        return HttpResponse("Unexpected server error")

