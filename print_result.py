import gmpy,urllib2

url1 = "http://localhost:5000/pub_params"
response1 = urllib2.urlopen(url1)
data = response1.read()
data = data[1:-1]
data = data.split(",")
r = int(data[2][:-1])
file = open('result.txt', 'r')
read = file.read()
read = read.split(" ")
c1 = int(read[0])
c2 = int(read[1])
x = int(read[2])
p = int(read[3])
cc1 = pow(c1,x,p)
g = 7
mm = (c2*gmpy.invert(cc1,p))%p
for i in range (0,100):
	gip = pow(g,i,p)
	if gip == mm:
		print "The result is " + str(i)
#print "The result is " + str(mm)