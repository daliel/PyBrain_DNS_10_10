import sys
from NET import *
from other import *
import os
import zmq
import numpy as np

ITERATIONS = 1000000

Net = None

def main(arg, path, iter, update = None):
	global lendata, data
	lendata = 0
	ITERATIONS = 1000000
	print (arg)	
	Net = NET(arg)
	if update == None:
		#path = os.getcwd()
		dirlist = os.listdir(path)
		l = []
		for i in dirlist:
			if os.path.isfile(i):
				if i[-4:] == "upd":
					l.append(os.path.basename(i))
		if len (l)>0:
			l1 = []
			for i in xrange(len(l)):
				l1.append(l[i][:-5].split("  "))
			d = dict(l1[:])
			l2 = d.keys()
			l2 = np.sort(np.array(l2, dtype = "float"))
			for i in l:
				if i.find(l2[0]) != -1:
					if d[l2[0]] == "%s_%s_%s"%(argv[0],x ,argv[1]):
						f2 = i
					break
		dirlist = os.listdir(path)
		l = []
		for i in dirlist:
			if os.path.isfile(i):
				if i[-4:] == "xml":
					l.append(os.path.basename(i))
		if len (l)>0:
			l1 = []
			for i in xrange(len(l)):
				l1.append(l[i][:-5].split("  "))
			d = dict(l1[:])
			l2 = d.keys()
			l2 = np.sort(np.array(l2, dtype = "float"))
			for i in l:
				if i.find(l2[0]) != -1:
					Net.UpdateWeights(i, f2)
					break
	if update != None:
		ITERATIONS = 0
		for i in xrange(len(arg[1:-1])):
			ITERATIONS += arg[i+1]
		ITERATIONS *= 100
		Net.Update(arg[1:-1], update)
		dirlist = os.listdir(path)
		l = []
		for i in dirlist:
			if os.path.isfile(i):
				if i[-4:] == "xml":
					l.append(os.path.basename(i))
		if len (l)>0:
			l1 = []
			for i in xrange(len(l)):
				l1.append(l[i][:-5].split("  "))
			d = dict(l1[:])
			l2 = d.keys()
			l2 = np.sort(np.array(l2, dtype = "float"))
			for i in l:
				if i.find(l2[0]) != -1:
					Net.UpdateWeights(i)
					break
	ReloadData(Net, path)
	context = zmq.Context()
	#socket_r = context.socket(zmq.SUB)
	#socket_r.bind("tcp://127.0.0.1:5645")
	#socket_r.setsockopt(zmq.SUBSCRIBE, '')
	#socket_r.RCVTIMEO = 250
	socket = context.socket(zmq.PUB)
	socket.connect("tcp://127.0.0.1:5410")
	lastfname = ""
	old_err  = 0
	count = 0
	err_count = 0
	first_step =0
	fr = open(path+"/dMSE.err", "r")
	l = fr.read()
	fr.close()
	count_max = 0
	for i in xrange(len(arg[1:-1])):
		count_max += arg[i+1]
	l = l[1:-1].split(",")
	print ("len DMSE", len(l))
	if len(l)>0 and l[0].isdigit() == True:
		for i in xrange(len(l)):
			l[i] = np.float64(l[i])
	for i in xrange(ITERATIONS):
		#err= Net.TrainNet(5, 0.000001)
		err= Net.TrainNetOnce()
		err_count=err_count - err
		if i == 0:
			old_err = err
		if i >1:
			if np.abs(SpeedLearning(err_count, i+1)) <= np.abs(err):
				msg = "%s %s %s %s %s %s %s"%(iter, err, arg, i, count, SpeedLearning(err_count, i+1), check_error(data, Net))
				socket.send(msg)
				break
		msg = "%s %s %s %s %s %s %s"%(iter, err, arg, i, count, SpeedLearning(err_count, i+1), check_error(data, Net))
		socket.send(msg)
		if i < len(l):
				if l[i]<err:
					count  = count_max
		if update ==None:
			
			if err >= old_err:
				count +=1
			else: count = 0
		else:
			if err == old_err:
				count +=1
			else: count = 0
		if count >= count_max:
			err = old_err
			msg = "%s %s %s %s %s %s %s"%(iter, err, arg, i, count, SpeedLearning(err_count, i+1), check_error(data, Net))
			socket.send(msg)
			break
		if i%(ITERATIONS/100) == 0:
			ReloadData(Net, path)
			fname = '%s  %s_%s_%s.work'%(Net.err, Net.inputsize, Net.hiden, Net.outputsize)
			if fname == lastfname:
				fnamecmp+=1
			else: fnamecmp = 0
			if fnamecmp>=2:
				
				msg = "%s %s %s %s %s %s %s"%(iter, err, arg, i, count, SpeedLearning(err_count, i+1), check_error(data, Net))
				socket.send(msg)
				break
			lastfname = fname
			Net.SaveNet(path+"/"+fname)
		old_err = err
	if update != None:
		fname = '%s  %s_%s_%s.upd'%(Net.err, Net.inputsize, Net.hiden, Net.outputsize)
		Net.SaveNet(path+"/"+fname)
	else:
		Net.SaveNet()
	print ("end %s        %s"%(arg, err))
	sys.exit()

def ReloadData(Net, path):
	global lendata, data
	print ("Begin loading data")
	fr = open(path+"/data.len", "r")
	d = fr.read()
	fr.close()
	d = d.split(", ")
	shape = []
	shape.append(int(d[0][1:]))
	shape.append(int(d[1][:-1]))
	res = np.loadtxt(path+"/data.txt", ndmin = 2)
	res = res.tolist()
	data = res[:]
	if lendata != len(res) or lendata == 0:
		Net.ds.clear()		
		r = Net.AddData(res[:-1], res[1:])
	lendata = len(res)
	print ("End loading data")
	
def check_error(data, net):
	e = []
	for i in xrange(1, len(data)-1):
		r = net.TestNet(data[i])
		e.append(r.mean())
	e = np.array(e)
	#print e.mean()
	e = (1-e.mean())*100
	return e
		
def sort_b(l):
		n = 1 
		while n < len(l):
			for i in range(len(l)-n):
				if l[i] > l[i+1]:
					l[i],l[i+1] = l[i+1],l[i]
			n += 1
		return l[:]

def SpeedLearning (s, t):
	return np.float64(s)/np.float64(t)	

def chunks(l, n):
	"""Yield successive n-sized chunks from l."""
	o = []
	for i in xrange(0, len(l), n):
		o.append(tuple(l[i:i+n]))
	return o