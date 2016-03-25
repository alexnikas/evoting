import requests
import random, gmpy, urllib2

def gen_prime(BITS):
    lb = 2 ** (BITS - 1)
    ub = (2 * lb)
    p = random.randrange(lb,ub)
    while gmpy.is_prime(p) == False:
        p = random.randrange(lb,ub)
        return p

url = "http://localhost:5000/secret-page?flag=0"
BITS = 2048

username = "admin"
password = "mypass"

response = requests.get(url, auth = (username, password), verify = False)
a = response
print a

url1 = "http://localhost:5000/pub_params"
response1 = urllib2.urlopen(url1)
data = response1.read()
data = data[1:-1]
data = data.split(",")
h = int(data[0][:-1])
p = int(data[1][:-1])
r = int(data[2][:-1])

#encrypt with ElGamal

m = input('Vote with 0 or 1: ')
g = 7
c1 = pow(g,r,p)
c2 = pow(h,r,p)
c2 = (c2 * pow(g,int(m),p)) % p
chiphertxt = str(c1) + "," + str(c2) + "," + str(p)

#RSA digital signature

p = gen_prime(BITS)
q = gen_prime(BITS)
n = p * q
fi = (p - 1) * (q - 1)
e = 2 ** 16 + 1
d = gmpy.invert(e,fi)
signature = pow(m,d,n)

#send data with get request

to_be_sent = str(chiphertxt) + "." + str(signature) + "." + str(n)
url = "http://localhost:5000/secret-page?flag=1"
url = str(url) + "&to_be_sent=" + str(to_be_sent)
response = requests.get(url, auth = (username, password), verify = False)

#print(url) #print(ciphertxt)