from Tkinter import *
from dialog import *
from multiprocessing import Process
from threading import Thread
import Proc
import zmq
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
		context = zmq.Context()
		self.socket = context.socket(zmq.SUB)
		self.socket.bind("tcp://127.0.0.1:5410")
		self.socket.setsockopt(zmq.SUBSCRIBE, '')
		self.socket.RCVTIMEO = 25
		self.Exit = False
		#self.learningrate = 0.1
		threads = [0]*self.MaxSimpleMul
		for i in xrange(self.MaxSimpleMul):
			threads[i] = Thread(target=self.Twork, args=(i, os.getcwd()+"/%s"%i))
			threads[i].start()
		self.root.mainloop()

	def PrepareFS(self):
		for i in xrange(self.MaxSimpleMul):
			if os.path.isdir(os.getcwd()+"/%s"%i) == False:
				os.mkdir(os.getcwd()+"/%s"%i)
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
		TextStructure = [0]*self.MaxSimpleMul
		TextIterations = [0]*self.MaxSimpleMul
		TextError = [0]*self.MaxSimpleMul
		TextMean = [0]*self.MaxSimpleMul
		for i in xrange(self.MaxSimpleMul):
			TextStructure[i] = StringVar()
			TextIterations[i] = StringVar()
			TextError[i] = StringVar()
			TextMean[i] = StringVar()
		for j in xrange(self.MaxSimpleMul):
			Label(self.SummuryInfo, textvariable = TextStructure[j]).grid(row=j+1, column=0)
			Label(self.SummuryInfo, textvariable = TextIterations[j]).grid(row=j+1, column=1)
			Label(self.SummuryInfo, textvariable = TextError[j]).grid(row=j+1, column=2)
			Label(self.SummuryInfo, textvariable = TextMean[j]).grid(row=j+1, column=3)
		self.SummuryInfo.grid()
		
			
		
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
				self.Mainproc[i] = Process(target=Proc.main, args = (arg, os.getcwd()+"/%s"%i, i, "main"))
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
			self.Mainproc[iter] = Process(target=Proc.main, args = (arg, os.getcwd()+"/%s"%iter, "main"))
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
		if self.StartButtonName.get() != "Start Network":
			try:
				msg = self.socket.recv()
				#print msg
				m = msg.split(" ")
				if m[0] == 'main':
					#print 
					TextStructure[iter].set("%s",m[2])
					TextIterations[iter].set("%s",m[3])
					TextError[iter].set("%s",m[1])
					TextMean[iter].set("%s",m[5])
					"""self.MainProcText.set("%s\n%s"%(m[2], m[1]))
					self.PorogText.set("Structure Hiden layer of NN: %s"%m[4])
					self.IterationText.set("Iteration i = %s"%m[3])
					self.MeanError.set("Mean of Errors = %s"%m[5])
					self.RealErrorText.set("Real Error = %s"%m[6])
					self.dMSE.append(float(m[1]))"""
			except: pass
		self.root.update()

	#def MainLoop(self):
		
	def DellFiles(self, path, fend, all = False):
		#path = os.getcwd()
		dirlist = os.listdir(path)
		l = []
		for i in dirlist:
			if os.path.isfile(i):
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
				os.remove(i)
			elif i.find("%s"%l2[0]) == -1:
				os.remove(i)
				
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
						if os.path.isfile(i):
							#print iter,  i[-3:], "ISFILE"
							if i[-3:] == "xml":
								print iter,  i, "ISFILE"
								l.append(os.path.basename(i))
					print iter, l, "L"
					l1=[]
					for i in xrange(len(l)):
						l1.append(l[i][:-4].split("  "))
					for i in xrange(len(l1)):
						l1[i][0] = float(l1[i][0])
					d = dict(l1[:])
					l2 = d.keys()
					l2 = np.sort(np.array(l2,dtype = "float"))
					print l2
					if l2[0]<0.000000000000001:
						self.Exit = True
						break
					fw = open("dMSE.err","w")
					fw.write("%s"%self.dMSE[iter][:-1])
					fw.close()
					self.dMSE[iter] = []
					param = self.ParamFromText(d[l2[0]])
					alter = self.Alternate(param[2])
					self.AddProc(iter, alter[:])
				p = 0
				if self.startedProc[iter] != []:
					for i in self.startedProc[iter]:
						if i.is_alive() == True:
							p+=1
					if p == 0:
						dirlist = os.listdir(path)
						l = []
						for i in dirlist:
							if os.path.isfile(i):
								if i[-3:] == "upd":
									l.append(os.path.basename(i))
						l1=[]
						for i in xrange(len(l)):
							l1.append(l[i][:-4].split("  "))
						for i in xrange(len(l1)):
							l1[i][0] = float(l1[i][0])
						d = dict(l1[:])
						l2 = d.keys()
						l2 = np.sort(np.array(l2,dtype = "float"))
						
						self.StartNN(d[l2[0]].split("_")[1])
						self.root.title("MAin 52x52 BackProp %s"%d[l2[0]].split("_")[1])
						self.startedProc[iter] = []
						DellFiles(path, "xml")
						DellFiles(path, "upd", True)
						DellFiles(path, "work")
			#self.UpdateButtons()
			self.root.update()
			self.UpdateMainProcNN(iter)

	def AddProc(self, iter, alter):
		self.startedProc[iter] = []
		for i in xrange(len(alter)):
			arg = []
			arg+=[10/self.MaxSimpleMul]																														#############
			arg+=alter[i]
			arg+=[10/self.MaxSimpleMul]																														#############
			self.startedProc[iter].append(Process(target=Proc.main, args=(arg, os.getcwd()+"/%s"%iter, i, i)))
		for i in  self.startedProc[iter]:
			print iter, i
			i.start()
		
	def ParamFromText(self, s):
		s1 = s.split("_")
		s2 = []
		print (s1, "ParamFromText")
		s2.append(int(s1[0]))
		s2.append(int(s1[2]))
			#else: s2.append(s1[i])
		s3 = s1[1].strip("[").strip("]")
		if s3.find(",") == -1:
			s2.append([int(s3)])
		else:
			s4 = s3.split(",")
			s5 = []
			for i in s4:
				s5.append(int(i))
			s2.append(s5)
		return s2[:]

	def Alternate(self, m):
		r = []
		for i in xrange(len(m)):
			m[i]= m[i]+1
			r.append(m[:])
			m[i]= m[i]-1
		m.append(1)
		r.append(m)
		
		return r
		
	def CommandStopProc(self, event):
		for i in xrange(len(self.ProcessButtons)):
			print (self.ProcessButtons[i], event.widget)
			if self.ProcessButtons[i] == event.widget:
				self.startedProc[iter][i].terminate()
				event.widget.destroy()
				break
			
if __name__ == "__main__":
	a = APP()