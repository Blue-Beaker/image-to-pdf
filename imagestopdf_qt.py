#! /bin/python3
import sys
from PIL import Image
import os
from PyQt5 import QtGui, QtWidgets,uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QResizeEvent,QStandardItemModel,QStandardItem,QKeyEvent
from PyQt5.QtCore import *


dir=os.path.dirname(sys.argv[0])
ui=os.path.join(dir,"imagestopdf.ui")

class App(QtWidgets.QMainWindow):
    
	addFileButton:QPushButton
	addFolderButton:QPushButton
	convertButton:QPushButton
	fileListWidget:QListWidget
	gridLayout:QGridLayout
	def __init__(self):
		super(App, self).__init__()
		uic.loadUi(ui, self)
		self.centralWidget().setLayout(self.gridLayout)
		self.addFileButton.clicked.connect(self.selectInputFile)
		self.addFolderButton.clicked.connect(self.selectInputFolder)
		self.convertButton.clicked.connect(self.selectConvertOutput)
		self.show()
	def keyPressEvent(self, a0: QKeyEvent) -> None:
		if a0.key()==16777223 and self.fileListWidget.hasFocus():	#Delete key
			self.fileListWidget.takeItem(self.fileListWidget.currentRow())
		return super().keyPressEvent(a0)
	
	def selectInputFile(self):
		dialog=QFileDialog(self)
		dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
		dialog.fileSelected.connect(self.addFile)
		dialog.filesSelected.connect(self.addFiles)
		dialog.show()

	def selectInputFolder(self):
		dialog=QFileDialog(self)
		dialog.setFileMode(QFileDialog.FileMode.DirectoryOnly)
		dialog.setOption(QFileDialog.Option.ShowDirsOnly,False)
		dialog.fileSelected.connect(self.addFolder)
		dialog.show()

	def addFiles(self,files:list[str]):
		for file in files:
			self.addFile(file)
	def addFile(self,file:str):
		try:
			image = Image.open(file)
			self.fileListWidget.addItem(file)
		except:
			pass
	def addFolder(self,folder:str):
		for file in sorted(os.listdir(folder)):
			self.addFile(os.path.join(folder,file))
			
	def selectConvertOutput(self):
		dialog=QFileDialog(self)
		dialog.setFileMode(QFileDialog.FileMode.AnyFile)
		dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
		dialog.setMimeTypeFilters(["application/pdf"])
		dialog.setNameFilters(["*.pdf"])
		dialog.fileSelected.connect(self.convert)
		dialog.show()

	def convert(self,pdf_path:str):				#convert function
		imagelist:list[Image.Image]=[]
		for index in range(self.fileListWidget.count()):
			item=self.fileListWidget.item(index)
			img=item.text()
			print(img)
			image = Image.open(img)
			im = image.convert('RGB')
			imagelist.append(im)
		if not pdf_path.endswith(".pdf"):
			pdf_path=pdf_path+".pdf"
		pdf_path=os.path.join(os.getcwd(),pdf_path)
		im1=imagelist.pop(0)
		im1.save(pdf_path,save_all=True, append_images=imagelist)

app = QtWidgets.QApplication(sys.argv)
window=App()

window.show()
app.exec()
