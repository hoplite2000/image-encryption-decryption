from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from encrypt import encrypt as en
from decrypt import decrypt as de

def imagelabel(path):
	image = Image.open(path)
	image = image.resize((500, 300))
	img = ImageTk.PhotoImage(image)
	imglabel.configure(image=img)
	imglabel.image = img

def encryptfun():
	global Resultvar
	try:
		enpath = en(Filevar.get())
		imagelabel(enpath)
		Resultvar.set("Saved encrypted image and key in Encrypted Images folder")
	except:
		messagebox.showerror("Error", "Error, Enter valid files")

def decryptfun():
	global Resultvar
	try:
		depath = de(Filevar.get(), Keyvar.get())
		imagelabel(depath)
		Resultvar.set("Saved decrypted image in Decrypted Images folder")
	except:
		messagebox.showerror("Error", "Error, Enter valid files")

def filebrowse():
	global Filevar
	Filevar.set(filedialog.askopenfilename(initialdir="~/", title="Select a File", filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("jpeg", "*.jpeg"), ("txt files", "*.txt"), ("all files", "*.*"))))

	imagelabel(Filevar.get())

def keybrowse():
	global Keyvar
	Keyvar.set(filedialog.askopenfilename(initialdir="~/", title="Select a File", filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("jpeg", "*.jpeg"), ("txt files", "*.txt"), ("all files", "*.*"))))

root = Tk()

root.geometry('700x625')
root.configure(background='#F0F8FF')
root.title('Image Encryption and Decryption')

Filevar = StringVar()
Keyvar = StringVar()
Resultvar = StringVar()

filelabel = Label(root, text='File', bg='#F0F8FF', font=('arial', 14, 'normal')).place(x=50, y=40)
fileinputlabel = Entry(root, textvariable=Filevar, bg='#F0F8FF', font=('arial', 14, 'normal'), width=42).place(x=100, y=40)
browsefile = Button(root, text='Browse', bg='#F0F8FF', font=('arial', 12, 'normal'), command=filebrowse).place(x=550, y=35)

keylabel = Label(root, text='Key', bg='#F0F8FF', font=('arial', 14, 'normal')).place(x=50, y=90)
keyinputlabel = Entry(root, textvariable=Keyvar, bg='#F0F8FF', font=('arial', 14, 'normal'), width=42).place(x=100, y=90)
browsekey = Button(root, text='Browse', bg='#F0F8FF', font=('arial', 12, 'normal'), command=keybrowse).place(x=550, y=85)

image = Image.open("bk.png")
image = image.resize((500,300))
img = ImageTk.PhotoImage(image)
imglabel = Label(image=img)
imglabel.image = img
imglabel.place(x=100, y=165)

result = Label(root, textvariable=Resultvar, bg='#F0F8FF', font=('arial', 14, 'normal'), width=50).place(x=100, y=500)

encrypt = Button(root, text='Encrypt', bg='#F0F8FF', font=('arial', 12, 'normal'), command=encryptfun).place(x=200, y=550)
decrypt = Button(root, text='Decrypt', bg='#F0F8FF', font=('arial', 12, 'normal'), command=decryptfun).place(x=425, y=550)

root.mainloop()