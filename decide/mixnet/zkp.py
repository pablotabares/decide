
import random
from mixnet import mixcrypt
import hashlib
from Crypto.Util.number import inverse
from Crypto.Math.Numbers import Integer
'''Non-interactive random oracle access for zero-knowledge proofs'''
k1=mixcrypt.MixCrypt()
p = int(k1.k.p)
g = int(k1.k.g)

secret='12345'
x=int(hashlib.md5(secret.encode()).hexdigest()[:8],16) % p

y= pow(g,x,p)
v = random.randint(1, p)
t = pow(g, v, p)
#Challenge
c = random.randint(1, p)
r = (v - c * x)
if (r < 0):
    
    Result=(inverse(pow(g,-r,p),p)* pow(y, c, p)) % p
else:
    Result = (pow(g, r, p) * pow(y, c, p)) % p
print('In this case Alice is the prover and Bob is the verifier')
print('The objective is to show Bob that Alice knows the secret but without revealing the secret to Bob')
print('======Agreed parameters============')
print('P=', p, '\t(Prime number)')
print('G=', g, '\t(Generator)')
print('======The secret==================')
print('x=', x, '\t(Alice\'s secret)')
print('======Random values===============')
print('c=', c, '\t(Bob\'s random value)')
print('v=', v, '\t(Alice\'s random value)')
print('======Shared value===============')
print('g^x mod P=\t', y)
print('r=\t\t', r)
print('=========Results===================')
print('t=g**v % p =\t\t', t)
print('( (g**r) * (y**c) )=\t', Result)
if (t == Result):
    print('Alice has proven she knows x')
else:
    print('Alice has not proven she knows x')
