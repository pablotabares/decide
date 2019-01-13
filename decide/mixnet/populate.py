import requests
import random
import itertools
from base import mods
from django.conf import settings
from .models import Auth, Mixnet
from django.contrib.auth.models import User
from census.models import Census
from django.utils import timezone
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
import re
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt

def createQuestion():
    # Create the Question
    q = Question(desc='pregunta 1')
    q.save()
    return q

# Create the possible answers
def createAnswers(q):
    answers = []
    for i in range(5):
        opt = QuestionOption(question=q, option='opción {}'.format(i + 1))
        opt.save()
        answers.append(opt)
    return answers

def createVotation(q):
    # Create the votings
    v = Voting(name='votación', question=q)
    v.start_date = timezone.now()
    v.save()
    return v

# Create the users
def createUsers(v):
    users = []
    for i in range(4):
        u, _ = User.objects.get_or_create(username='usuario {}'.format(i + 1))
        u.is_active = True
        u.set_password('usuario {}'.format(i + 1))
        u.save()
        users.append(u)
        c = Census(voter_id=u.id, voting_id=v.id)
        c.save()
    return users






