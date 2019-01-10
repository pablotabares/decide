from Crypto.Util.number import inverse
from django.views import View


from django.conf import settings
from django.shortcuts import get_object_or_404
import hashlib
from mixnet.zkp_form import ZKPForm
from mixnet.mixcrypt import rand


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MixnetSerializer
from .models import Auth, Mixnet, Key
from base.serializers import KeySerializer, AuthSerializer

from django.shortcuts import render
from django.shortcuts import render_to_response


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

        data = {"key": {"p": mn.key.p, "g": mn.key.g}}
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

        return Response(KeySerializer(pubkey, many=False).data)


class Shuffle(APIView):

    def post(self, request, voting_id):
        """
         * voting_id: id
         * msgs: [ [int, int] ]
         * pk: { "p": int, "g": int, "y": int } / nullable
         * position: int / nullable
        """

        position = request.data.get("position", 0)
        mn = get_object_or_404(
            Mixnet, voting_id=voting_id, auth_position=position)

        msgs = request.data.get("msgs", [])
        pk = request.data.get("pk", None)
        if pk:
            p, g, y = pk["p"], pk["g"], pk["y"]
        else:
            p, g, y = mn.key.p, mn.key.g, mn.key.y

        msgs = mn.shuffle(msgs, (p, g, y))

        data = {
            "msgs": msgs,
            "pk": {"p": p, "g": g, "y": y},
        }
        # chained call to the next auth to gen the key
        resp = mn.chain_call("/shuffle/{}/".format(voting_id), data)
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

        position = request.data.get("position", 0)
        mn = get_object_or_404(
            Mixnet, voting_id=voting_id, auth_position=position)

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
            "pk": {"p": p, "g": g, "y": y},
        }
        # chained call to the next auth to gen the key
        resp = mn.chain_call("/decrypt/{}/".format(voting_id), data)
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
