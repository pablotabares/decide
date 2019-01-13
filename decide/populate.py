from census.models import Census
from django.contrib.auth.models import User

def populateUsers():
    f = open("populateData\\users", "r")
    for line in f:
        array = line.split("|")
        User.objects._create_user(array[0], array[1], array[2])

def populateCensus():
    #Census.objects.create(voting_id=, voter_id=)
    return None