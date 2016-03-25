from flask import Flask
from functools import wraps
from flask import request, Response
app = Flask(__name__)
from passlib.apps import custom_app_context as pwd_context
import requests
import random, gmpy

def gen_prime(BITS):
    lb=2**(BITS-1)
    ub=(2*lb)
    p=random.randrange(lb,ub)
    while gmpy.is_prime(p)==False:
        p=random.randrange(lb,ub)
        return p

#basic variable initialisation

#sum_c2 = 1
#sum_c1 = 1
e = 2 ** 16 + 1
bits = 2048
p = gen_prime(bits)
x = random.randrange(p)
count = 0

def gen_key():
    g = 7
    r = random.randrange(p)
    h = pow(g,x,p)
    keys = [h, p, r]
    return keys

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    hash = pwd_context.encrypt("mypass")
    print hash
    if username == 'admin' and pwd_context.verify(password, hash):
        return True
    else:
        return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/pub_params')
def pub_params():
    return str(public_key)

@app.route('/secret-page')
@requires_auth
def secret_page():
    global count
    flag = str(request.args.get('flag'))
    #print "----------------------------------" + str(flag=="1")
    if flag == "1":
        to_be_received = str(request.args.get('to_be_sent'))
        a = to_be_received.split(".")
        #print "lenght is: " + str(len(a))
        ciphertext = a[0]
        signature = int(a[1])
        n = int(a[2])
        validation = str(pow(signature,e,n))
        #print "validation = " + str(validation)
        b = ciphertext.split(",")
        c1 = int(b[0])
        c2 = int(b[1])
        p = int(b[2])
        val = ["0", "1"]
        if validation in val:
            if count != 0:
                file = open('result.txt', 'r')
                read = file.read()
                read = read.split(" ")
                sum_c1 = int(read[0])
                sum_c2 = int(read[1])
                sum_c2 = (int(c2) * int(sum_c2))%p
                sum_c1 = (int(c1) * int(sum_c1))%p
                file.close()
                file = open("result.txt", "w")
                file.write(str(sum_c1) + " " + str(sum_c2) + " " + str(x) + " " + str(p))
                file.close()
            else:
                sum_c2 = int(c2)
                sum_c1 = int(c1)
                file = open("result.txt", "w")
                file.write(str(sum_c1) + " " + str(sum_c2) + " " + str(x) + " " + str(p))
                file.close()
                count = 1
    return "Success"
if __name__ == "__main__":
    public_key = gen_key()
    app.run()