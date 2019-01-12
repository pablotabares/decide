from django.db import models

from .mixcrypt import MixCrypt

from base import mods
from base.models import Auth, Key
from base.serializers import AuthSerializer
from django.conf import settings


# number of bits for the key, all auths should use the same number of bits
B = settings.KEYBITS

# Mixnet model
# A Mixnet works both as a list of authorities and as a local authority; as such, it holds the methods required by an authority to work
class Mixnet(models.Model):
    # The ID this mixnet is assigned to
    voting_id = models.PositiveIntegerField()
    # The position the authority represented by this model has in the authority chain
    auth_position = models.PositiveIntegerField(default=0)
    # The authorities included in this mixnet
    auths = models.ManyToManyField(Auth, related_name="mixnets")
    # The private key of the local authority
    key = models.ForeignKey(Key, blank=True, null=True,
                            related_name="mixnets",
                            on_delete=models.SET_NULL)
    # The public key of the mixnet
    pubkey = models.ForeignKey(Key, blank=True, null=True,
                               related_name="mixnets_pub",
                               on_delete=models.SET_NULL)

    # String representation of a mixnet
    def __str__(self):
        auths = ", ".join(a.name for a in self.auths.all())
        return "Voting: {}, Auths: {}\nPubKey: {}".format(self.voting_id,
                                                          auths, self.pubkey)

    # Shuffles and encrypts a message
    def shuffle(self, msgs, pk):
        crypt = MixCrypt(bits=B)
        k = crypt.setk(self.key.p, self.key.g, self.key.y, self.key.x)

        return crypt.shuffle(msgs, pk)

    # Shuffles and decrypts a message
    def decrypt(self, msgs, pk, last=False):
        crypt = MixCrypt(bits=B)
        k = crypt.setk(self.key.p, self.key.g, self.key.y, self.key.x)
        return crypt.shuffle_decrypt(msgs, last)

    # Given the key parameters, creates and sets the key for the local authority
    def gen_key(self, p=0, g=0):
        crypt = MixCrypt(bits=B)
        if self.key:
            k = crypt.setk(self.key.p, self.key.g, self.key.y, self.key.x)
        elif (not g or not p):
            k = crypt.genk()
            key = Key(p=int(k.p), g=int(k.g), y=int(k.y), x=int(k.x))
            key.save()

            self.key = key
            self.save()
        else:
            k = crypt.getk(p, g)
            key = Key(p=int(k.p), g=int(k.g), y=int(k.y), x=int(k.x))
            key.save()

            self.key = key
            self.save()

    # Makes a chain call, asking every auth in sequence to do the required operation
    # This method is called after doing the operation in this authority
    def chain_call(self, path, data):
        next_auths=self.next_auths()

        data.update({
            "auths": AuthSerializer(next_auths, many=True).data,
            "voting": self.voting_id,
            "position": self.auth_position + 1,
        })

        if next_auths:
            auth = list(next_auths)[0].url
            r = mods.post('mixnet', entry_point=path,
                           baseurl=auth, json=data)
            return r

        return None
    
    # Returns the next authority in the chain
    def next_auths(self):
        next_auths = self.auths.filter(me=False)

        if self.auths.count() == next_auths.count():
            next_auths = next_auths[1:]

        return next_auths

class ConnectionStatus(models.Model):
    auth = models.ForeignKey(Auth, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.BooleanField()

    def __str__(self):
        return (str(self.status)+ ", "+str(self.auth) +", date: " +str(self.date))