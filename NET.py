from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.datasets import SupervisedDataSet, SequentialDataSet
from pybrain.structure.connections import FullConnection
from pybrain.supervised.trainers import RPropMinusTrainer, BackpropTrainer
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer
import xml.etree.ElementTree as ET
import numpy as np



class NET():
	def __init__(self, arg):
		self.inputsize = arg[0]
		self.outputsize = arg[-1]
		self.hiden = arg[1:-1]
		self.err = 1
		self.old_err = 1
		b = []
		b.append(self.inputsize)
		b+=self.hiden
		b.append(self.outputsize)
		#print b#"%s, %s, %s, hiddenclass=TanhLayer"%(self.inputsize, self.hiden, self.outputsize)
		self.net = FeedForwardNetwork()
		self.inputlayer = LinearLayer(self.inputsize, "Input")
		self.net.addInputModule(self.inputlayer)
		self.outputlayer = LinearLayer(self.outputsize, "Output")
		self.net.addOutputModule(self.outputlayer)
		self.hidenlayers = []
		for i in xrange(len(self.hiden)):
			self.hidenlayers.append(SigmoidLayer(self.hiden[i], "hiden%s"%i))
			self.net.addModule(self.hidenlayers[-1])
		self.net.addConnection(FullConnection(self.inputlayer, self.outputlayer))
		for i in xrange(len(self.hidenlayers)):
			self.net.addConnection(FullConnection(self.inputlayer, self.hidenlayers[i]))
			self.net.addConnection( FullConnection(self.hidenlayers[i], self.outputlayer))
		for i in xrange(len(self.hidenlayers)):
			for j in xrange(i+1, len(self.hidenlayers)):
				self.net.addConnection(FullConnection(self.hidenlayers[i], self.hidenlayers[j]))
				#self.print_conections(self.net)
		self.net.sortModules()
		self.ds = SupervisedDataSet(self.inputsize, self.outputsize)

	def Update(self, hiden, h):
		self.net = FeedForwardNetwork()
		self.inputlayer = LinearLayer(self.inputsize, "Input")
		self.net.addInputModule(self.inputlayer)
		self.outputlayer = LinearLayer(self.outputsize, "Output")
		self.net.addOutputModule(self.outputlayer)
		self.hidenlayers = []
		for i in xrange(len(hiden)):
			self.hidenlayers.append(SigmoidLayer(hiden[i], "hiden%s"%i))
			self.net.addModule(self.hidenlayers[-1])
		self.net.addConnection(FullConnection(self.inputlayer, self.outputlayer))
		for i in xrange(len(self.hidenlayers)):
			self.net.addConnection(FullConnection(self.inputlayer, self.hidenlayers[i]))
			self.net.addConnection( FullConnection(self.hidenlayers[i], self.outputlayer))
		for i in xrange(len(self.hidenlayers)):
			for j in xrange(i+1, len(self.hidenlayers)):
				if i<h:
					self.net.addConnection(FullConnection(self.hidenlayers[i], self.hidenlayers[j]))
				elif i == h:
					self.net.addConnection(FullConnection(self.hidenlayers[i], self.hidenlayers[j], inSliceTo=hiden[i]-1))
				else:
					self.net.addConnection(FullConnection(self.hidenlayers[i], self.hidenlayers[j]))
				#self.print_conections(self.net)
		self.net.sortModules()
		self.hiden = hiden
		
	def print_conections(self, n):
		print ("BEGIN")
		for mod in n.modules:
			print (mod)
			for conn in n.connections[mod]:
				print (conn)
				for cc in range(len(conn.params)):
					print (conn.whichBuffers(cc), conn.params[cc])
		print ("END")

	def AddData(self, datainput, dataoutput, learningrate):
		if len(dataoutput) != len(datainput):
			print ("Not equals data", len(dataoutput), len(datainput))
			return 1
		self.ds = SupervisedDataSet(self.inputsize, self.outputsize)
		for i in xrange(len(dataoutput)):
			self.ds.appendLinked(datainput[i], dataoutput[i])
		self.trainer = BackpropTrainer(self.net, dataset = self.ds, learningrate = learningrate)
		return 0
	
 
 
	def TrainNet(self, epoch, error):		
		
		if epoch<=5 : 
			epoch = 5
		i = 0
		count = 0
		while i< epoch:
			if error == self.err:
				break
			self.err = self.trainer.train()
			if self.err == self.old_err:
				count +=1
			else: count = 0
			if count == 3:
				self.err = self.old_err
				return (self.err, 1)
			self.old_err = self.err
			i+=1
		#self.SaveNet('%s  %s_%s_%s.work'%(self.err, self.inputsize, self.hiden, self.outputsize))
		return [self.err, 0]

	def TrainNetOnce(self):		
		
		self.err = self.trainer.train()
		
		return self.err

	def SaveNet(self, filename = None):
		if filename == None:
			NetworkWriter.writeToFile(self.net, '%s  %s_%s_%s.xml'%(self.err, self.inputsize, self.hiden, self.outputsize))
		else:
			NetworkWriter.writeToFile(self.net, filename)	
		
	def LoadNet(self, fname):
		self.net = NetworkReader.readFrom(fname) 
		tree = ET.parse(fname)
		x = tree.getroot()
		l = []
		for modules in x.findall('Network/Modules/SigmoidLayer/dim'):
			l.append(int(modules.get("val")))
		self.hiden = l[:]
		self.inputsize = self.net.indim
		self.outputsize = self.net.outdim

	def TestNet(self, inp):
		if len(inp)!= self.inputsize:
			return 0		
		return self.net.activate(inp[:])
		
	def UpdateWeights(self, f1, f2 = None):
		n = NetworkReader.readFrom(f1)
		if f2 != None:
			n2 = NetworkReader.readFrom(f2)
		
		def DictParams(n):
			l1 = []
			for mod in n.modules:
				l = []
				for conn in n.connections[mod]:
					
					if conn.paramdim > 0:
					
						l.append([conn.outmod.name, conn.params])
				d = dict(l)
				l1.append([mod.name, d])
			d1 = dict(l1)
			return d1
			
		d1 = DictParams(n)
		if f2 != None:
			d2 = DictParams(n2)
		d3 = DictParams(self.net)
		
		params = np.array([])
		if f2 != None:
			for i in d2:
				for j in d2[i]:
					try:
						b = d3[i][j][:]
						b[:d2[i][j].size] = d2[i][j][:]
						d3[i].update({j:b})
					except: pass
		for i in d1:
			for j in d1[i]:
				try:
					b = d3[i][j][:]
					b[:d1[i][j].size] = d1[i][j][:]
					d3[i].update({j:b})
				except: pass
		for i in d3["Input"]:
			params = np.hstack((params,d3["Input"][i]))
		for i in xrange(len(self.hiden)):
			for j in d3["hiden%s"%i]:
				params = np.hstack((params,d3["hiden%s"%i][j]))
		self.net._setParameters(params)
		
		

if __name__ == '__main__':
	global lendata
	lendata = 0
	#print "Begin loading data"
	from other import *
	Net = NET(45,45,"%s"%([1]))
	out = read_file_data_r_maxima("data.txt")
	if lendata != len(out) or lendata == 0:
		Net.ds.clear()
		res = [0 for i in xrange(len(out)/5)]
		j=0
		for i in xrange(0, len(out), 5):
			res[j] = tuple(IntListToTrans_45(out[i:i+5]))
			j+=1
		#inx, res = CreateRegression(res[:])
	
		r = Net.AddDataSequential(res[:])
	lendata = len(out)
	
	del out
	#print "End loading data"