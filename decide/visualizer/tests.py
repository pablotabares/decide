from django.test import TestCase

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase
import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
import json

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from store.models import Vote
from rest_framework.authtoken.models import Token

class VisualizerTestCase(BaseTestCase):

    #Method copy from voting/test.py
    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    #Method copy from voting/test.py
    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user


    def test(self):
        #Create and save question
        q = Question(desc='Question1')
        q.save()

        #Create and save question options
        for i in range(2):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()

        #Create and save votation with question
        v = Voting(name='Votation1')
        v.save()

        v.questions.add(q)

        #Add auth to votation and save it
        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        #Create and save multiple voters for votation
        for i in range(2):
            u, _ = User.objects.get_or_create(username='Voter{}'.format(i+1))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

        #...
        #Votation created
        #...

        #Start votation
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        #...
        #Votation started
        #...

        #Method copy from voting/test.py
        #Create and add votes
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()
        clear = {}
        for opt in v.questions.first().options.all():
            clear[opt.number] = 0
            for i in range(2):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                #voter = voters.pop()
                mods.post('store', json=data)


        #Login with admin
        self.login()

        #Tally Done
        v.tally_votes()
        
        #...
        #Votation ended
        #...
        
        #Method for test views's method
        response = self.client.get('/visualizer/{}/'.format(v.pk))
        self.assertEqual(response.status_code, 200)

        #Check 1
        self.assertEqual(response.context['voting_id'], v.pk)

        #Check 2
        self.assertEqual('Votation1' in response.context['voting'].values() , True)

        #Check 3
        varTemp = response.context['voting']
        self.assertEqual('Question1' in varTemp['questions'][0].values() , True)

        #Test Finished OK
        
        
        
        

       
        

        


        


        


        
       

        


        

