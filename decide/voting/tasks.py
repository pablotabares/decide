from celery import Celery
from base import mods
from django.conf import settings
from django.shortcuts import get_object_or_404
import os


app = Celery('tasks', BROKER_URL=settings.REDIS_URL,
             CELERY_RESULT_BACKEND=settings.REDIS_URL)


@app.task
def tally(voting_id, token):
    voting = get_object_or_404(Voting, pk=voting_id)
    votes = voting.get_votes(token)

    auth = voting.auths.first()
    shuffle_url = "/shuffle/{}/".format(voting.id)
    decrypt_url = "/decrypt/{}/".format(voting.id)
    auths = [{"name": a.name, "url": a.url} for a in voting.auths.all()]

    # first, we do the shuffle
    data = {"msgs": votes}
    response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                         response=True)
    if response.status_code != 200:
        # TODO: manage error
        pass

    # then, we can decrypt that
    data = {"msgs": response.json()}
    response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                         response=True)

    if response.status_code != 200:
        # TODO: manage error
        pass

    voting.tally = response.json()
    voting.save()

    voting.do_postproc()
