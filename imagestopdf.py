#! /bin/python3
import sys
from xxlimited import Str
from PIL import Image
import glob
import os
import tkinter
from tkinter import ttk,StringVar,filedialog
import tkinter.messagebox
import ctypes
defaultextension="*.png"
def dirSel():				#Select folder
	pathVar.set(filedialog.askdirectory())
	pathBox.insert(0,"")
def outFileSel():				#Select output file
	outFileVar.set(filedialog.asksaveasfilename(filetypes=["PDF {*.pdf}"],confirmoverwrite=1,title="Save PDF"))
	outFileBox.insert(0,"")
def convert(path,pdf_path="output.pdf",namefilter=defaultextension,gui=0):				#convert function
	global debugBox
	imagelist=[]
	for img in sorted(glob.glob(os.path.join(os.getcwd(),path,namefilter))):
		print(img)
		if gui:
			debugBox.insert("end",img)
		image = Image.open(img)
		im = image.convert('RGB')
		imagelist.append(im)
	pdf_path=os.path.join(os.getcwd(),pdf_path)
	if os.path.exists(pdf_path):
		if gui:
			replace=tkinter.messagebox.askokcancel("Replace?",f'"{pdf_path}" exists. Replace?')
		else:
			replace=input("Replace?[y/N]").lower() in ["y","yes"]
		if replace:
			os.remove(pdf_path)
		else:
			print("Canceled.")
			sys.exit(0)
	im1=imagelist.pop(0)
	im1.save(pdf_path,save_all=True, append_images=imagelist)
	if gui:
		debugBox.insert("end","Completed")
		debugBox.see(debugBox.size())
if len(sys.argv)>=2:
	if len(sys.argv)>=3:
		output=sys.argv[2]
	else:
		output="output.pdf"
	if len(sys.argv)>=4:
		convert(os.path.join(os.getcwd(),sys.argv[1]),output,sys.argv[3])
	else:
		convert(os.path.join(os.getcwd(),sys.argv[1]),output)
	sys.exit(0)
	
root=tkinter.Tk()

try:#windows
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
except:
    ScaleFactor=75
style=ttk.Style()
try:
    style.theme_use("vista")
except:
    style.theme_use("default")

pathVar=StringVar()
outFileVar=StringVar()
nameFilterVar=StringVar(value=defaultextension)
pathLabel=ttk.Label(root,text="Path")
pathLabel.place(relx=0,rely=0,relwidth=1,relheight=0.1)
pathBox=ttk.Entry(pathLabel,textvariable=pathVar)
pathBox.place(relx=0.2,rely=0,relwidth=0.7,relheight=1)
outFileLabel=ttk.Label(root,text="Output")
outFileLabel.place(relx=0,rely=0.1,relwidth=1,relheight=0.1)
outFileBox=ttk.Entry(outFileLabel,textvariable=outFileVar)
outFileBox.place(relx=0.2,rely=0,relwidth=0.7,relheight=1)
nameFilterLabel=ttk.Label(root,text="Filter")
nameFilterLabel.place(relx=0,rely=0.2,relwidth=1,relheight=0.1)
nameFilterBox=ttk.Entry(nameFilterLabel,textvariable=nameFilterVar)
nameFilterBox.insert(0,"")
nameFilterBox.place(relx=0.2,rely=0,relwidth=0.8,relheight=1)
pathSelectButton=ttk.Button(pathLabel,text="...",command=dirSel)
pathSelectButton.place(relx=0.9,rely=0,relwidth=0.1,relheight=1)
outFileSelectButton=ttk.Button(outFileLabel,text="...",command=outFileSel)
outFileSelectButton.place(relx=0.9,rely=0,relwidth=0.1,relheight=1)
convertButton=ttk.Button(root,text="Convert",command=lambda :convert(path=pathVar.get(),pdf_path=outFileVar.get(),gui=1,namefilter=nameFilterVar.get()))
convertButton.place(relx=0,rely=0.3,relwidth=1,relheight=0.1)
debugBox=tkinter.Listbox(root)
debugBox.place(relx=0,rely=0.4,relwidth=1,relheight=0.6)

root.geometry("300x300+100+100")
root.title("Images to PDF")
root.mainloop()
