from django import forms


class ZKPForm(forms.Form):
    secret = forms.CharField(label='Random secret', max_length=20)
    primes = ((31, 31), (119, 119), (571, 571),
              (1889, 1889), (27277, 27277), (63337, 63337))
    prime = forms.ChoiceField(label='Choice a prime number', choices=primes)
    r1 = forms.IntegerField(label='Alice\'s random number',min_value=1)
    r2 = forms.IntegerField(label='Bob\'s random challenge',min_value=1)
