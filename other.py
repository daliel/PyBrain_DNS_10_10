# -*- coding: utf-8 -*-
import numpy as np

def MaxSimpleMul(x):
	y = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
	if type(x) == list:
		lx = len(x)
	else: lx = x
	for i in range(len (y)-1, -1, -1):
		if lx >y[i]:
			if lx%y[i] == 0:
				return y[i]
	
def ZIP(x, y):
	print x
	lx = len(x)
	print lx
	x = np.array(x).reshape((1, lx))
	print x, " NP"
	x.reshape((lx/y,y))
	print x, "NP.reshape"
	
	
def Convulation(X, Y):
	return map(lambda a,b:a*b, X,Y[::-1])

def TransToIntList(e):
	a = []
	sa  = sum(e)/len(e)
	if len(e)<52:
		return -1
	for i in range(52):
		if e[i] > sa:
			a.append(i+1)
	return a

def TransToIntList_80(e):
	a = []
	sa  = sum(e)/len(e)
	if len(e)<80:
		return -1
	for i in range(80):
		if e[i] > sa:
			a.append(i+1)
	return a
	
def TransToIntList_10(e):
	a = []
	sa  = sum(e)/len(e)
	if len(e)<10:
		return -1
	for i in range(10):
		if e[i] > sa:
			a.append(i)
	return a
	
def TransToIntList_45(e):
	a = []
	sa  = sum(e)/len(e)
	if len(e)<45:
		return -1
	for i in range(45):
		if e[i] > sa:
			a.append(i+1)
	return a
	
def IntListToTrans_52( e):
	a = [0 for i in xrange(52)]
	if type(e) == list:
		for j in xrange(len(e)):
			a[e[j]-1]=1
	else:
		a[e-1]=1
	return a[:] 
	
def IntListToTrans_45( e):
	a = [0 for i in xrange(45)]
	if type(e) == list:
		for j in xrange(len(e)):
			a[e[j]-1]=1
	else:
		a[e-1]=1
	return a[:]

def IntListToTrans_80( e):
	a = [0 for i in xrange(80)]
	if type(e) == list:
		for j in xrange(len(e)):
			a[e[j]-1]=1
	else:
		a[e-1]=1
	return a[:] 

def IntListToTrans_10( e):
	a = [0 for i in xrange(10)]
	if type(e) == list:
		for j in xrange(len(e)):
			a[e[j]]=1
	else:
		a[e-1]=1
	return a[:] 
	
def IntListToTrans42( e):
	a = [0 for i in xrange(42)]
	if type(e) == list:
		for j in xrange(len(e)):
			a[e[j]-1]=1
	else:
		a[e-1]=1
	return a[:] 
	
def create_pattern_52_1(d):
	k = [[] for i in xrange(len(d))]
	for i in xrange(len(d)):
		k[i].append(IntListToTrans_52(d[i]))
	return k[:]
	
def create_pattern_52(d):
	k = [[] for i in xrange(len(d))]
	for i in xrange(len(d)):
		
		k[i].append(IntListToTrans_52(d[i][2:8]))
	return k[:]
	
def create_pattern_42(d):
	k = [[] for i in xrange(len(d))]
	for i in xrange(len(d)):
		
		k[i].append(IntListToTrans42(d[i][0:6]))
	return k[:]
	
def create_pattern_6(d):
	k = [[] for i in xrange(len(d)-1)]
	for i in xrange(len(d)-1):
		k[i].append(d[i])
		k[i].append(d[i+1])
	return k[:]

def read_file_data(fname):
	result = []
	fr = open(fname, "r")
	buf = fr.readlines()
	fr.close()
	i = 0
	while i<len(buf):
		temp = buf[i].split(" ")
		temp1 = []
		for n in range(2,11):
			if temp[n] == 'А':
				temp[n] = 0
			if temp[n] == "Б":
				temp[n] = 1
			if n == 11:
				temp[n] = float(temp[n])
			temp1.append(int(temp[n]))
		result.append(temp1)
		i+=1
	return result
	
def read_file_data_megalot(fname):
	result = []
	fr = open(fname, "r")
	buf = fr.readlines()
	fr.close()
	i = 0
	while i<len(buf):
		temp = buf[i].split(",")
		temp1 = []
		for n in range(0,7):
			temp1.append(int(temp[n]))
		result.append(temp1)
		i+=1
	return result
	
def read_file_data_r(fname):
	result = []
	fr = open(fname, "r")
	buf = fr.readlines()
	fr.close()
	i = len(buf)-1
	#print i
	while i>-1:
		temp = buf[i].split(" ")
		temp1 = []
		for n in range(2,10):
			if temp[n] == 'А':
				temp[n] = 0
			if temp[n] == "Б":
				temp[n] = 1
			temp1.append(int(temp[n]))
		result.append(temp1)
		i-=1
	return result

def read_file_data_r_1(fname):
	result = []
	fr = open(fname, "r")
	buf = fr.readlines()
	fr.close()
	i = len(buf)-2
	#print i
	temp1 = []
	while i>-0:
		temp = buf[i].split("\t")
		for n in range(4,10):
			temp1.append(int(temp[n]))
		i-=1
	return temp1[:]

def read_file_data_r_maxima(fname):
	result = []
	fr = open(fname, "r")
	buf = fr.readlines()
	fr.close()
	i = len(buf)-2
	#print i
	temp1 = []
	while i>0:
		#print buf[i]
		temp = buf[i].split("\t")
		for n in range(4,9):
			
			temp1.append(int(temp[n]))
		i-=1
	return temp1[:]
	
def read_file_data_r_keno(fname):
	result = []
	fr = open(fname, "r")
	buf = fr.readlines()
	fr.close()
	i = len(buf)-2
	#print i
	temp1 = []
	while i>0:
		#print buf[i]
		temp = buf[i].split("\t")
		for n in range(4,24):
			
			temp1.append(int(temp[n]))
		i-=1
		#print temp1[-1]
	return temp1[:]
	
def read_file_data_troika(fname):
	result = []
	fr = open(fname, "r")
	buf = fr.readlines()
	fr.close()
	i = len(buf)-2
	#print i
	temp1 = []
	while i>0:
		#print buf[i]
		temp = buf[i].split("\t")
		for n in range(4,7):
			
			temp1.append(int(temp[n]))
		i-=1
	return temp1[:]
	
def demo():
	# Teach network XOR function
   
	tr = read_file_data("data.txt")
	p=create_pattern(tr)
	# create a network with two input, two hidden, and one output nodes
	for i in xrange(1, 52*52):
		n = NN(6, i, 52)
		# train it with some patterns
		print n.ni, n.nh, n.no, i
		n.train(patterns = p, iterations = i*1000)
		# test it
		n.test(p)
		n.save("%i_z.txt"%i)
		#n.load("z.txt")
		n.test(p)
def CreateRegressionData_maxima(data):
	maxima = 45
	maxlen = 20
	empty = [0]*maxima
	inp = []
	outp = []
	i = 1
	while i<len(data):
		tmp = [0]*(maxlen*maxima)
		#print "begin", len(tmp)
		#for j in xrange(700-i):
		#	 tmp[j*maxima:(j*maxima)+maxima] = empty[:]
		#print "begin", len(tmp)
		z = i
		
		while z>0 and z>i-maxlen:
			outp.append(data[z])
			j=z
			if z>maxlen:
				t = []*(maxlen*maxima)
			else: t = []*(z*maxima)
			k = 1
			while j>0 and j>z-maxlen:
				#print "len(data[j-1])", len(data[j-1])
				t[-k*maxima:(-k*maxima)+maxima]=data[j-1][:]
				j-=1
				k+=1
			tmp[-len(t):] = t[:]
			#print len(tmp)
			inp.append(tmp)
			z-=1
		i+=1
	print len(inp)
	return inp[:], outp[:]

def CreateRegressionData_52(data):
	maxima = 52
	maxlen = 20
	empty = [0]*maxima
	inp = []
	outp = []
	i = 1
	while i<len(data):
		tmp = [0]*(maxlen*maxima)
		#print "begin", len(tmp)
		#for j in xrange(700-i):
		#	 tmp[j*maxima:(j*maxima)+maxima] = empty[:]
		#print "begin", len(tmp)
		z = i
		
		while z>0 and z>i-maxlen:
			outp.append(data[z])
			j=z
			if z>maxlen:
				t = []*(maxlen*maxima)
			else: t = []*(z*maxima)
			k = 1
			while j>0 and j>z-maxlen:
				#print "len(data[j-1])", len(data[j-1])
				t[-k*maxima:(-k*maxima)+maxima]=data[j-1][:]
				j-=1
				k+=1
			tmp[-len(t):] = t[:]
			#print len(tmp)
			inp.append(tmp)
			z-=1
		i+=1
	print len(inp)
	return inp[:], outp[:]

def CreateRegressionData_keno(data):
	maxima = 80
	maxlen = 20
	empty = [0]*maxima
	inp = []
	outp = []
	i = 1
	while i<len(data):
		tmp = [0]*(maxlen*maxima)
		#print "begin", len(tmp)
		#for j in xrange(700-i):
		#	 tmp[j*maxima:(j*maxima)+maxima] = empty[:]
		#print "begin", len(tmp)
		z = i
		
		while z>0 and z>i-maxlen:
			outp.append(data[z])
			j=z
			if z>maxlen:
				t = []*(maxlen*maxima)
			else: t = []*(z*maxima)
			k = 1
			while j>0 and j>z-maxlen:
				#print "len(data[j-1])", len(data[j-1])
				t[-k*maxima:(-k*maxima)+maxima]=data[j-1][:]
				j-=1
				k+=1
			tmp[-len(t):] = t[:]
			#print len(tmp)
			inp.append(tmp)
			z-=1
		i+=1
	print len(inp)
	return inp[:], outp[:]
	
if __name__ == "__main__":
	x = [0, 0, 1, 0, 0, 0, 1, 0, 1, 0]
	ZIP(x,5)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
