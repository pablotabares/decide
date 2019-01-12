import requests
from .models import Auth, Mixnet, ConnectionStatus
import re
import datetime
from autotask.tasks import periodic_task

# Returns a dictionary with key/value pairs authority/status

def pingAuths():
    # Retrieves all authorities from the database
    auths = Auth.objects.all()
    # Initializes dictionary of auths/
    reached_auths = {}
    regexp = re.compile(".*localhost.*")
    for auth in auths:
        if(regexp.search(auth.url) == None):
            try:
                r = requests.get(auth.url)
                if r.status_code == requests.codes.ok:
                    reached_auths[auth] = "ONLINE"
                else:
                    reached_auths[auth] = "OFFLINE"
            except:
                reached_auths[auth] = "OFFLINE"
        else:
            reached_auths[auth] = "LOCAL"

    return reached_auths


def mixnetStatus():
    #We get all the mixnets from the database
    mixnets = Mixnet.objects.all()

    mixnets_status = {}
    regexp = re.compile(".*localhost.*")
    for mixnet in mixnets:
        #Checking the status of every authority of a mixnet
        for auth in mixnet.auths.all():
            reached_auths = {}
            if(regexp.search(auth.url) == None):
                try:
                    r = requests.get(auth.url)
                    if r.status_code == requests.codes.ok:
                        reached_auths[auth] = "ONLINE"
                    else:
                        reached_auths[auth] = "OFFLINE"
                except:
                    reached_auths[auth] = "OFFLINE"
            else:
                reached_auths[auth] = "LOCAL"
        
        #If only one of the auths is offline, the mixnet will be offline
        if 'OFFLINE' in reached_auths.values():
            mixnets_status[mixnet.voting_id] = "OFFLINE"
        else:
            mixnets_status[mixnet.voting_id] = "ONLINE"
    
    return mixnets_status


#Every 5 minutes, we will store the status of all the authorities
@periodic_task(seconds=300)
def updateConnections():
     # Retrieves all authorities from the database
    auths = Auth.objects.all()

    regexp = re.compile(".*localhost.*")
    for auth in auths:
        status = False
        if(regexp.search(auth.url) == None):
            try:
                r = requests.get(auth.url)
                if r.status_code == requests.codes.ok:
                    status = True
                else:
                    status = False
            except:
                status = False
        else:
            status = True
        c = ConnectionStatus(auth=auth, date=datetime.datetime.now(), status=status)
        c.save()