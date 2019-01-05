import requests
from .models import Auth
import re

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
