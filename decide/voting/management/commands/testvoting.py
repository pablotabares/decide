import random
import itertools

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone

from base import mods
from base.models import Auth
from census.models import Census
from mixnet.mixcrypt import MixCrypt
from mixnet.mixcrypt import ElGamal
from voting.models import Voting, Question, QuestionOption


class Command(BaseCommand):
    help = 'Test the full voting process with one auth (self)'

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        # Creation of questions test for the voting
        q = Question(desc='test question')
        q2 = Question(desc='test question 2')

        # Saving the questions before adding them to the voting
        q.save()
        q2.save()

        # Creation of question options per each question previouly created
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i + 1))
            opt.save()

        for n in range(5):
            opt2 = QuestionOption(question=q2, option='option {}'.format(n + 1))
            opt2.save()

        # Creation and storage of voting
        v = Voting(name='test voting', desc='testeo de voting')
        v.save()

        # Addition of the questions created to the voting
        v.questions.add(q)
        v.questions.add(q2)

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()
        clear = {}
        for q in v.questions.all():
            for opt in q.options.all():
                clear[opt.number] = 0
                for i in range(random.randint(0, 5)):
                    a, b = self.encrypt_msg(opt.number, v)
                    data = {
                        'voting': v.id,
                        'voter': voter.voter_id,
                        'vote': {'a': a, 'b': b},
                    }
                    clear[opt.number] += 1
                    user = self.get_or_create_user(voter.voter_id)
                    self.login(user=user.username)
                    voter = voters.pop()
                    mods.post('store', json=data)

        return clear

    def handle(self, *args, **options):
        print("Creating voting")
        v = self.create_voting()
        self.create_voters(v)

        print("Creating pubkey")
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        print("Storing votes")
        clear = self.store_votes(v)
        print("Tally")
        v.tally_votes()

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        print("Result:")
        for q in v.question.options.all():
            print(" * {}: {} tally votes / {} emitted votes".format(q, tally.get(q.number, 0),
                                                                    clear.get(q.number, 0)))

        print("")
        print("Postproc Result:")
        for q in v.postproc:
            print(" * {}: {} postproc / {} votes".format(q["option"], q["postproc"], q["votes"]))
