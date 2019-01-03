from multiping import MultiPing
from .models import Auth
import re

def pingAuths():
        # Retrieves all authorities from the database
        auths = Auth.objects.all()

        # Makes a list of the authority urls
        urls = []
        # We skip localhost entries
        regexp = re.compile(".*localhost.*")
        for auth in auths:
            if(regexp.search(auth.url) == None):
                urls.append(auth.url)

        # Checks whether or not it can reach the authorities
        # Compiles a dictionary with the auths and whether or not they've been reached
        reached_auths = {}
        # If there are any authorities to reach:
        if(len(urls) > 0):
            # Creates the multiping object with the retrieved urls
            mp = MultiPing(urls, ignore_lookup_errors= True)

            # Send the pings to those addresses
            mp.send()

            # Wait for responses with a 5 second timeout
            responses, no_responses = mp.receive(5)

            
            for auth in auths:
                # If reached, saves the time taken
                if (auth.url in responses.keys()):
                    reached_auths[auth] = responses[auth]
                # Otherwise, saves None
                else:
                    reached_auths[auth] = None

        # If there are no authorities to reach:
        else:
            for auth in auths:
                reached_auths[auth] = 0
        # Returns the ping results
        return reached_auths