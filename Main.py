from Tkinter import *
from dialog import *
from multiprocessing import Process, Value, Array
from threading import Thread
import Proc
import time
#import zmq
import socket
import os
from tkFileDialog import *
from NET import *
from other import *
from dialog import *


class APP:
	def __init__(self):
		self.root = Tk()
		self.root.title("MAin 10x10 BackProp")
		self.lframe = Frame(self.root)
		self.rframe = Frame(self.root)
		self.StartButtonName = StringVar()
		self.StartButtonName.set("Start Network")
		self.StartButton = Button(self.root, textvariable = self.StartButtonName, command=self.StartNN)
		self.StartButton.grid()
		self.TestButton = Button(self.root, text = "Load Nn and Test", command = self.TestNN)
		self.TestButton.grid()
		self.TestText = StringVar()
		self.MaxSimpleMul = MaxSimpleMul(10)										###################
		self.PrepareFS()
		self.PrepareView()
		self.Mainproc = [None]*self.MaxSimpleMul
		self.startedProc = [0] *self.MaxSimpleMul
		for i in xrange(self.MaxSimpleMul) :
			self.startedProc[i] = []
		self.socket = socket.socket()
		self.socket.bind(("", 8011))
		self.socket.listen(100)#(self.MaxSimpleMul)
		self.Exit = False
		#self.learningrate = 0.1
		self.threads = [0]*self.MaxSimpleMul
		self.learningrate = [0.01]*self.MaxSimpleMul
		
		b=[]
		for i in xrange(7):
			b.append(Value("d", 1.))
		self.sharedmemory = [b]* self.MaxSimpleMul
		for i in xrange(self.MaxSimpleMul):
			self.threads[i] = Thread(target=self.Twork, args=(i, os.getcwd()+"/%s"%i))
			self.threads[i].daemon = True
			self.threads[i].start()
		self.root.protocol('WM_DELETE_WINDOW', self.Quit)
		self.root.mainloop()

	def PrepareFS(self):
		for i in xrange(self.MaxSimpleMul):
			if os.path.isdir(os.getcwd()+"/%s"%i) == False:
				os.mkdir(os.getcwd()+"/%s"%i)
				fw = open(os.getcwd()+"/%s/dMSE.err"%i, "w")
				fw.write("%s"%[1])
				fw.close()
		out = read_file_data_troika("data.txt")
		res = [0 for i in xrange(len(out)/3)]
		j=0
		for i in xrange(0, len(out), 3):
			res[j] = tuple(IntListToTrans_10(out[i:i+3]))
			j+=1
		res = np.array(res)
		for i in xrange(self.MaxSimpleMul):
			np.savetxt(os.getcwd()+"/%s/data.txt"%i, res[:,i*(10/self.MaxSimpleMul):i*(10/self.MaxSimpleMul)+(10/self.MaxSimpleMul)])     #############
			fw = open(os.getcwd()+"/%s/data.len"%i, "w")
			fw.write("%s"%list(res[:,i*(10/self.MaxSimpleMul):i*(10/self.MaxSimpleMul)+(10/self.MaxSimpleMul)].shape))                               ##################
			fw.close()
			
	def PrepareView(self):
		self.SummuryInfo = Frame(self.root)
		Label(self.SummuryInfo, text= "Structure NN").grid( row=0, column=0)
		Label(self.SummuryInfo, text= "Iteration").grid( row=0, column=1)
		Label(self.SummuryInfo, text= "Error").grid( row=0, column=2)
		Label(self.SummuryInfo, text= "Mean Errors").grid( row=0, column=3)
		self.TextStructure = [0]*self.MaxSimpleMul
		self.TextIterations = [0]*self.MaxSimpleMul
		self.TextError = [0]*self.MaxSimpleMul
		self.TextMean = [0]*self.MaxSimpleMul
		for i in xrange(self.MaxSimpleMul):
			self.TextStructure[i] = StringVar()
			self.TextIterations[i] = StringVar()
			self.TextError[i] = StringVar()
			self.TextMean[i] = StringVar()
		for j in xrange(self.MaxSimpleMul):
			Label(self.SummuryInfo, textvariable = self.TextStructure[j]).grid(row=j+1, column=0)
			Label(self.SummuryInfo, textvariable = self.TextIterations[j]).grid(row=j+1, column=1)
			Label(self.SummuryInfo, textvariable = self.TextError[j]).grid(row=j+1, column=2)
			Label(self.SummuryInfo, textvariable = self.TextMean[j]).grid(row=j+1, column=3)
		self.SummuryInfo.grid(sticky=N+S+E+W)
		
			
		
	def StartNN(self, x = [1], iter=None):
		if self.StartButtonName.get() == "Start Network":
			self.StartButtonName.set("Pause Network")
			self.root.title("MAin 10x10 RPMSProp")																##############
		
		if iter == None:
			arg =[]
			arg += [10/self.MaxSimpleMul]																			############
			arg +=x
			arg += [10/self.MaxSimpleMul]																			#########	
			
			self.dMSE = [0]*self.MaxSimpleMul
			for i in xrange(self.MaxSimpleMul):
				#threads[i] = Thread(target=self.Twork, args=(i, os.getcwd()+"/%s"%i))
				self.Mainproc[i] = Process(target=Proc.main, args = (arg, os.getcwd()+"/%s"%i, "main", i, 0.1))
				self.dMSE[i] = []
			for i in xrange(self.MaxSimpleMul):
				#threads[i].start()
				self.Mainproc[i].start()
			
		if iter != None:
			self.dMSE[iter] = []
			arg =[]
			arg += [10/self.MaxSimpleMul]																			############
			arg +=x
			arg += [10/self.MaxSimpleMul]																			###########
			self.Mainproc[iter] = Process(target=Proc.main, args = (arg, os.getcwd()+"/%s"%iter, "main", iter, self.learningrate[iter], None, self.sharedmemory))
			self.Mainproc[iter].start()

		
	def TestNN(self):
		
		options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
		options['initialdir'] = os.getcwd()
		options['initialfile'] = 'myfile.txt'
		options['parent'] = self.root
		options['title'] = 'This is a title'
		p = askopenfile( **options)
		Net = NET(1,1)
		Net.LoadNet(p.name)
		d = DialogTestNN(self.root)
		res = IntListToTrans_52(d.value)
		#print len(res)
		t = Net.TestNet(res)
		print ("sizeinput = %s\n out = %s"%(Net.inputsize, t))
		t1 = t.tolist()
		s1 = []
		for i in xrange(len(t1)):
			s1.append((float(t1[i]), i+1))
		dd = dict(s1)	
		s = dd.keys()
		s = np.sort(np.array(s, dtype = "float"))
		r = []
		for i in range(1,7):
			r.append(dd[s[-i]])
			print (dd[s[-i]], s[-i])
		k = "%s\n%s"%(TransToIntList(t.tolist()), r)
		self.TestText.set("%s"%k)
	
	def UpdateButtons(self):
		if self.startedProc[iter] != []:
			try:
				msg = self.socket.recv()
				k = msg.split(" ")
				self.ButtonsText[int(k[0])].set("Net: %s, %s, %s\nError: %s\nProgress: %s"%(self.ParamForText[int(k[0])][0], self.ParamForText[int(k[0])][1], self.ParamForText[int(k[0])][2], float(k[1]), int(k[2])))
				self.root.update()
			except: pass
		
	def UpdateMainProcNN(self, iter):
		#self.TextStructure[int(m[2])].set("%s"%m[7])
		self.TextIterations[iter].set("%s"%self.sharedmemory[iter][3].value)
		self.TextError[iter].set("%s"%self.sharedmemory[iter][1].value)
		self.TextMean[iter].set("%s"%self.sharedmemory[iter][5].value)
		
		

	#def MainLoop(self):
		
	def DellFiles(self, path, fend, all = False):
		#path = os.getcwd()
		dirlist = os.listdir(path)
		l = []
		for i in dirlist:
			#if os.path.isfile(i):
			if i[-len(fend):] == fend:
				l.append(os.path.basename(i))
		l1=[]
		for i in xrange(len(l)):
			l1.append(l[i][:-(len(fend)+1)].split("  "))
		for i in xrange(len(l1)):
			l1[i][0] = float(l1[i][0])
		d = dict(l1[:])
		l2 = d.keys()
		l2 = np.sort(np.array(l2,dtype = "float"))
		for i in l:
			if all == True:
				os.remove(path+"/"+i)
			elif i.find("%s"%l2[0]) == -1:
				try:
					os.remove(path+"/"+i)
				except: 
					print path, i, "CAN'T REMOVE"
				
	def Twork(self, iter, path):
		#path = os.getcwd()
		while self.Exit == False:
			if self.Mainproc[iter] != None:
				#print self.Mainproc.is_alive()
				if self.Mainproc[iter].is_alive() == False and self.startedProc[iter] == []:
					dirlist = os.listdir(path)
					#print iter, dirlist
					l = []
					for i in dirlist:
						#print i
						if i[-4:]== ".xml":							
							l.append(i)
					#print iter, l, "L"
					l1=[]
					for i in xrange(len(l)):
						l1.append(l[i][:-4].split("  "))
					for i in xrange(len(l1)):
						l1[i][0] = float(l1[i][0])
					d = dict(l1[:])
					l2 = d.keys()
					l2 = np.sort(np.array(l2,dtype = "float64"))
					#print l2
					if l2[0]<0.000000000000001:
						self.Exit = True
						break
					fw = open("dMSE.err","w")
					fw.write("%s"%self.dMSE[iter][:-1])
					fw.close()
					self.dMSE[iter] = []
					learningrate = float("{0:.9f}".format(float(l2[0])/10))
					if self.learningrate[iter] > learningrate:
						self.learningrate[iter] = learningrate
					param = self.ParamFromText(d[l2[0]].split("_")[1])
					alter = self.Alternate(param)
					self.AddProc(iter, alter[:])
				p = 0
				if self.startedProc[iter] != []:
					for i in self.startedProc[iter]:
						if i.is_alive() == True:
							p+=1
					if p == 0 and self.Mainproc[iter].is_alive() == False:
						#print "YES"
						dirlist = os.listdir(path)
						l = []
						for i in dirlist:
								if i[-4:] == ".upd":
									l.append(i)
						l1=[]
						for i in xrange(len(l)):
							l1.append(l[i][:-4].split("  "))
						for i in xrange(len(l1)):
							l1[i][0] = float(l1[i][0])
						d = dict(l1[:])
						l2 = d.keys()
						l2 = np.sort(np.array(l2,dtype = "float64"))
						print d[l2[0]].split("_")
						arg = self.ParamFromText(d[l2[0]].split("_")[1])
						self.StartNN(arg, iter)
						k =[10/self.MaxSimpleMul]
						k+=arg
						k.append(10/self.MaxSimpleMul)
						self.TextStructure[iter].set("%s"%k)
						#self.root.title("MAin 52x52 BackProp %s"%d[l2[0]].split("_")[1])
						self.StopProc(iter)
						self.startedProc[iter] = []
						self.DellFiles(path, "xml")
						self.DellFiles(path, "upd", True)
						self.DellFiles(path, "work")
			self.UpdateMainProcNN(iter)
						
	def AddProc(self, iter, alter):
		self.startedProc[iter] = []
		for i in xrange(len(alter)):
			arg = []
			arg+=[10/self.MaxSimpleMul]																														#############
			arg+=alter[i]
			arg+=[10/self.MaxSimpleMul]																														#############
			self.startedProc[iter].append(Process(target=Proc.main, args=(arg, os.getcwd()+"/%s"%iter, i, iter, self.learningrate[iter], i)))
		for i in  self.startedProc[iter]:
			#print iter, i
			i.start()
		
	def ParamFromText(self, s):
		s2 = []
		if s.find(",") == -1:
			s2.append(int(s[1:-1]))
		else:
			s1 = s[1:-1]
			s4 = s1.split(",")
			for i in s4:
				s2.append(int(i))
		return s2[:]

	def Alternate(self, m):
		r = []
		for i in xrange(len(m)):
			m[i]= m[i]+1
			r.append(m[:])
			m[i]= m[i]-1
		m.append(1)
		r.append(m)
		#print r
		return r
		
	def CommandStopProc(self, event):
		for i in xrange(len(self.ProcessButtons)):
			print (self.ProcessButtons[i], event.widget)
			if self.ProcessButtons[i] == event.widget:
				self.startedProc[iter][i].terminate()
				event.widget.destroy()
				break
				
	def Quit(self):
		self.Exit = True
		
		for i in xrange(self.MaxSimpleMul):
			self.threads[i].join()
			self.Mainproc[i].join()
		sys.exit()
			
if __name__ == "__main__":
	a = APP()