# Tau ide for omega

#from decimal import Decimal
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox
import tauLauncher, time

class Tau(Tk):
	def __init__(self, text_title= "Untitled"):
		super().__init__()
		self.text_title = text_title
		self.state('zoomed')
		self.title('Tau IDE - ' + self.text_title)
		self.iconbitmap('omega_file.ico')

		self.text = Text(self, bg= "#111111", fg= "#fff", insertbackground= "#fff")
		self.text.pack(expand= True, fill= 'both')

		self.MainMenu = Menu(self)
		self.fileMenu = Menu(self.MainMenu, tearoff=0)
		self.fileMenu.add_command(label= "New File", accelerator= "Ctrl+N")
		self.fileMenu.add_command(label= "Open File", accelerator= "Ctrl+O", command= self.open_file)
		self.fileMenu.add_command(label= "Save File", accelerator= "Ctrl+S", command= self.save)
		self.fileMenu.add_command(label= "Save As", accelerator= "Ctrl+Shift+S", command= self.save_as)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label= "Close Window", accelerator= "Ctrl+Shift+W", command= self.exit)
		self.MainMenu.add_cascade(label= "File", menu=self.fileMenu)

		self.editMenu = Menu(self.MainMenu, tearoff=0)
		self.editMenu.add_command(label= "Undo")
		self.editMenu.add_command(label= "Redo")
		self.editMenu.add_separator()
		self.editMenu.add_command(label= "Copy", accelerator= "Ctrl+C")
		self.editMenu.add_command(label= "Paste", accelerator= "Ctrl+V")
		self.MainMenu.add_cascade(label= "Edit", menu=self.editMenu)

		self.toolsMenu = Menu(self.MainMenu, tearoff=0)
		self.toolsMenu.add_command(label= "Build", accelerator= "Ctrl+B", command= self.runCode)
		self.MainMenu.add_cascade(label= "Tools", menu= self.toolsMenu)

		self.fileMenu.bind_all("<Control-o>", lambda event:self.open_file())
		self.fileMenu.bind_all("<Control-s>", lambda event:self.save())
		self.fileMenu.bind_all("<Control-S>", lambda event:self.save_as())
		self.fileMenu.bind_all("<Control-W>", lambda event:self.exit())
		self.toolsMenu.bind_all("<Control-b>", lambda event:self.runCode())

		'''
		EXPERIMENTAL - don't touch
		self.text.bind_all("(", lambda event:self.addRight(")"))
		self.text.bind_all("[", lambda event:self.addRight("]"))
		self.text.bind_all("\"", lambda event:self.addRight("\""))
		self.text.bind_all("'", lambda event:self.addRight("'"))
		self.text.bind_all("{", lambda event:self.addRight("}"))
		'''

		self.config(menu= self.MainMenu)

		if text_title != "Untitled": self.open_title()

	def exit(self):
		self.destroy()

	def runCode(self):
		self.save()
		self.lower()
		if self.text_title == "Untitled": return messagebox.showerror("Error", "File must be saved to run")
		code = self.text.get('1.0', END)
		if '.py' in self.text_title:
			exec(code)
			return
		tauLauncher.run(self.text_title, code)

	def open_file(self):
		with open("settings.txt")as f:
			lastDir = f.read()
		new_title = askopenfilename(initialdir= lastDir)

		if not new_title: return 

		with open(new_title) as f:
			new_text = f.read()
		if self.text_title != "Untitled":
			Tau(text_title= new_title)
		else:
			self.text_title = new_title
			self.title('Tau IDE - ' + self.text_title)
			self.text.delete('1.0', END)
			self.text.insert('1.0', new_text)
			with open("settings.txt", 'w') as f:
				f.write(self.text_title)

	def open_title(self):
		self.title('Tau IDE - ' + self.text_title)

		with open(self.text_title) as f:
			new_text = f.read()
		self.text.delete('1.0', END)
		self.text.insert('1.0', new_text)

	def save(self):
		if self.text_title == "Untitled":
			self.save_as()
		else:
			with open(self.text_title, 'w') as file:
				file.write(self.text.get('1.0', END))
			self.title('Tau IDE - ' + self.text_title + "                Saved!")
			time.sleep(.6)
			self.title('Tau IDE - ' + self.text_title)

	def save_as(self):
		files = [("Omega Files", ".omega")]
		new_title = asksaveasfile(filetypes= files, defaultextension = files)
		if new_title:
			self.text_title = new_title.name
		self.title('Tau IDE - ' + self.text_title)
		with open(self.text_title, 'w') as file:
			file.write(self.text.get('1.0', END))

	def addRight(self, char):
		self.text.insert(END, char)
		pos1 = self.text.index(INSERT)
		print(pos1)
		newPos = str(Decimal(pos1) - Decimal("0.1"))
		print(newPos)
		self.text.mark_set("insert", newPos)

app = Tau()
app.mainloop()