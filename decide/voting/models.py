from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver

from base import mods
from base.models import Key, Auth
from django.http import JsonResponse

IMPORTANCE_CHOICES = (
    (0, ("None")),
    (1, ("Not relevant")),
    (2, ("Review")),
    (3, ("May relevant")),
    (4, ("Relevant")),
    (5, ("Leading candidate"))
)


class Question(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    unlockquestion = models.ManyToManyField(Question, related_name='unlockquestion', blank=True)
    number = models.PositiveIntegerField(blank=True, null=True)
    #Adding the weight of this option
    weight = models.IntegerField( blank=False, null=True)
    importance = models.FloatField(choices=IMPORTANCE_CHOICES, default=0)

    option = models.TextField()

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)


class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    isWeighted = models.BooleanField(default=False)
    questions = models.ManyToManyField(Question, related_name='voting')

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [{"name": a.name, "url": a.url} for a in self.auths.all()],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes]

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''


        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = {"msgs": votes}


        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                             response=True)


        if response.status_code != 200 and len(votes) >0:

            # TODO: manage error necesitamos unir las api, para ver que se haga bien cuando no hay votaciones
            error_response = "error: Shuffle fails"
            return error_response
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                             response=True)

        if response.status_code != 200 and len(votes) >0 :
            # TODO: manage error, necesitamos unir las api, para ver que se haga bien cuando no hay votaciones
            error_response = "error: Decrypt fails"
            return error_response
            pass

        self.tally = response.json()
        self.save()
        self.do_postproc()
        return 'Voting tallied'


    def do_postproc(self):
        tally = self.tally
        for q in self.questions.all():
            options = q.options.all()

            opts = []
            for opt in options:
                if isinstance(tally, list):
                    votes = tally.count(opt.number)
                else:
                    votes = 0
                opts.append({
                    'option': opt.option,
                    'number': opt.number,
                    'votes': votes
                })

            # we have two types of tally the wheighted one or the traditional
            if not self.isWeighted:
                data = {'type': 'IDENTITY', 'options': opts}
            else:
                data = {'type': 'WEIGHT', 'options': opts}

            postp = mods.post('postproc', json=data)

            self.postproc = postp
            self.save()

    def __str__(self):
        return self.name
