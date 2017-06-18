from Tkinter import *
import string

class DialogCreateNN(Toplevel):
	def __init__(self, parent, title = "Create NN"):
		Toplevel.__init__(self, parent)
		self.transient(parent)
		#if title:
		#	self.title(title)
		self.parent = parent
		self.result = None
		body = Frame(self)
		self.initial_focus = self.body(body)
		Label(body, text = "Enter input nodes").pack()
		self.Text = Entry(body, width = 5 )
		self.Text.pack()
		Label(body, text = "Enter output nodes").pack()
		self.Text1 = Entry(body, width = 5 )
		self.Text1.pack()
		body.pack(padx=5, pady=5)
		self.value=[0]* 2
		self.buttonbox()
		#self.grab_set()
		if not self.initial_focus:
			self.initial_focus = self
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
		self.initial_focus.focus_set()
		self.Text.focus_set()
		self.wait_window(self)
		
	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden
		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons
		box = Frame(self)
		w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)
		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		box.pack()
	#
	# standard button semantics

	def ok(self, event=None):
		
		self.withdraw()
		self.update_idletasks()
		self.parent.focus_set()
		self.value[0] = int(self.Text.get())
		self.value[1] = int(self.Text1.get())
		self.destroy()
		
	def cancel(self, event=None):
		# put focus back to the parent window
		self.parent.focus_set()
		self.value = None
		self.destroy()

class DialogCreateNNWithHiden(Toplevel):
	def __init__(self, parent, title = "Create NN"):
		Toplevel.__init__(self, parent)
		self.transient(parent)
		#if title:
		#	self.title(title)
		self.parent = parent
		self.result = None
		body = Frame(self)
		self.initial_focus = self.body(body)
		Label(body, text = "Enter input nodes").pack()
		self.Text = Entry(body, width = 5 )
		self.Text.pack()
		Label(body, text = "Enter hiden nodes").pack()
		self.Text1 = Entry(body, width = 5 )
		self.Text1.pack()
		Label(body, text = "Enter output nodes").pack()
		self.Text2 = Entry(body, width = 5 )
		self.Text2.pack()
		body.pack(padx=5, pady=5)
		self.value=[0]* 3
		self.buttonbox()
		#self.grab_set()
		if not self.initial_focus:
			self.initial_focus = self
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
		self.initial_focus.focus_set()
		self.Text.focus_set()
		self.wait_window(self)
		
	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden
		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons
		box = Frame(self)
		w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)
		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		box.pack()
	#
	# standard button semantics

	def ok(self, event=None):
		
		self.withdraw()
		self.update_idletasks()
		self.parent.focus_set()
		self.value[0] = int(self.Text.get())
		self.value[1] = "[%s]"%(self.Text1.get())
		self.value[2] = int(self.Text2.get())
		self.destroy()
		
	def cancel(self, event=None):
		# put focus back to the parent window
		self.parent.focus_set()
		self.value = None
		self.destroy()
		
class Dialog(Toplevel):
	def __init__(self, parent, title = "Input"):
		Toplevel.__init__(self, parent)
		self.transient(parent)
		#if title:
		#	self.title(title)
		self.parent = parent
		self.result = None
		body = Frame(self)
		self.initial_focus = self.body(body)
		Label(body, text = "Enter input nodes").pack()
		self.Text = Entry(body, width = 20 )
		self.Text.pack()
		body.pack(padx=5, pady=5)
		self.value=[]
		self.buttonbox()
		self.grab_set()
		if not self.initial_focus:
			self.initial_focus = self
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
		self.initial_focus.focus_set()
		self.Text.focus_set()
		self.wait_window(self)
		
	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden
		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons
		box = Frame(self)
		w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)
		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		box.pack()
	#
	# standard button semantics

	def ok(self, event=None):		
		self.withdraw()
		self.update_idletasks()
		self.parent.focus_set()
		self.value = string.split(self.Text.get()," ")
		d =[]
		for i in xrange(len(self.value)):
			d.append(int(self.value[i]))
		self.value = d[:]
		self.destroy()
		
	def cancel(self, event=None):
		# put focus back to the parent window
		self.parent.focus_set()
		self.value = None
		self.destroy()

class DialogMegaLot(Toplevel):
	def __init__(self, parent, title = "Input"):
		Toplevel.__init__(self, parent)
		self.transient(parent)
		#if title:
		#	self.title(title)
		self.parent = parent
		self.result = None
		body = Frame(self)
		self.initial_focus = self.body(body)
		Label(body, text = "Enter input nodes").pack()
		self.Text = Entry(body, width = 20 )
		self.Text.pack()
		body.pack(padx=5, pady=5)
		self.value=[]
		self.buttonbox()
		self.grab_set()
		if not self.initial_focus:
			self.initial_focus = self
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
		self.initial_focus.focus_set()
		self.Text.focus_set()
		self.wait_window(self)

	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden
		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons
		box = Frame(self)
		w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)
		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		box.pack()
	#
	# standard button semantics

	def ok(self, event=None):
		self.withdraw()
		self.update_idletasks()
		self.parent.focus_set()
		self.value = string.split(self.Text.get(),",")
		d =[]
		for i in xrange(len(self.value)):
			d.append(int(self.value[i]))
		self.value = d[:]
		self.destroy()

	def cancel(self, event=None):
		# put focus back to the parent window
		self.parent.focus_set()
		self.value = None
		self.destroy()

class DialogProgressBar(Toplevel):
	def __init__(self, parent, title = "Input"):
		Toplevel.__init__(self, parent)
		self.transient(parent)
		#if title:
		#	self.title(title)
		self.parent = parent
		self.result = None
		body = Frame(self)
		self.initial_focus = self.body(body)
		Label(body, text = "Enter input nodes").pack()
		self.Text = Entry(body, width = 20 )
		self.Text.pack()
		body.pack(padx=5, pady=5)
		self.value=[]
		self.buttonbox()
		self.grab_set()
		if not self.initial_focus:
			self.initial_focus = self
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
		self.initial_focus.focus_set()
		self.Text.focus_set()
		self.wait_window(self)
		
	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden
		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons
		box = Frame(self)
		w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)
		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		box.pack()
	#
	# standard button semantics

	def ok(self, event=None):		
		self.withdraw()
		self.update_idletasks()
		self.parent.focus_set()
		self.value = string.split(self.Text.get()," ")
		d =[]
		for i in xrange(len(self.value)):
			d.append(int(self.value[i]))
		self.value = d[:]
		self.destroy()
		
	def cancel(self, event=None):
		# put focus back to the parent window
		self.parent.focus_set()
		self.value = None
		self.destroy()
	 
class DialogTestNN(Toplevel):
	def __init__(self, parent, title = "Input"):
		Toplevel.__init__(self, parent)
		self.transient(parent)
		self.parent = parent
		self.result = None
		fr = open("data.txt", "r")
		buf = fr.readlines()
		fr.close()
		i = len(buf)-2
		self.temp1 = []
		while i>0:
			self.temp1.append(buf[i].split("\t"))
			i-=1
		body = Frame(self)
		#Label(body, text = "Enter input nodes").pack()
		self.listbox = Listbox(body, width = 90)
		self.listbox.pack(side=TOP, padx=0, pady=0)
		for item in self.temp1:
			self.listbox.insert(END, item)
		self.initial_focus = self.body(body)
		
		#self.Text = Entry(body, width = 20 )
		#self.Text.pack()
		body.pack(padx=5, pady=5)
		self.update()
		self.value=[]
		self.buttonbox()
		self.grab_set()
		if not self.initial_focus:
			self.initial_focus = self
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
		self.initial_focus.focus_set()
		#self.Text.focus_set()
		self.wait_window(self)
		
	#
	# construction hooks

	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden
		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons
		
		box = Frame(self)
		w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)
		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)
		box.pack()
	#
	# standard button semantics

	def ok(self, event=None):		
		self.withdraw()
		self.update_idletasks()
		self.parent.focus_set()
		#self.value = self.listbox.curselection()
		d = []
		for i in range(4,10):
			d.append(int(self.temp1[self.listbox.curselection()[0]][i]))
		self.value = d
		self.destroy()
		
	def cancel(self, event=None):
		# put focus back to the parent window
		self.parent.focus_set()
		self.value = None
		self.destroy()
		
if __name__ == "__main__":
	root = Tk()
	d = DialogTestNN(root)
	print (d.value)