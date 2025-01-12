
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget,QLabel,QApplication,QWidget,QPushButton,QVBoxLayout,QHBoxLayout,QFileDialog
from PyQt5.QtGui import QPixmap
import os
from PIL.ImageQt import ImageQt
from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import (BLUR,CONTOUR,DETAIL,EDGE_ENHANCE,EDGE_ENHANCE_MORE,
                             EMBOSS,FIND_EDGES,SMOOTH,SMOOTH_MORE,SHARPEN,GaussianBlur, UnsharpMask)
#////////////////////////////////
app = QApplication([])
main_win = QWidget()
main_win.resize(700,500)
label_win = QLabel("Картинка")
list_of_fotos = QListWidget()
main_win.setWindowTitle("Easy Editor")
#////////////////////////////////
btn_folder = QPushButton("Папка")
btn_left = QPushButton("Лево")
btn_right = QPushButton("Резкость")
btn_flip = QPushButton("Зеркало")
btn_right2 = QPushButton("Право")
btn_bw = QPushButton("Ч/Б")
#////////////ЛЭЙАУТЫ/////////////////
HLayout = QHBoxLayout()
HLayout2 = QHBoxLayout()
VLayout = QVBoxLayout()
VLayout2 = QVBoxLayout()
HLayout.addWidget(btn_folder,alignment = Qt.AlignCenter)
HLayout2.addWidget(list_of_fotos)
HLayout2.addWidget(btn_flip)
HLayout.addWidget(label_win)
HLayout2.addWidget(btn_bw)
HLayout2.addWidget(btn_left)
HLayout2.addWidget(btn_right)
HLayout2.addWidget(btn_right2)
VLayout.addLayout(HLayout,500)
VLayout.addLayout(HLayout2,500)



workdir = ''
#/////////Функции///////////
def filter(files,extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
def showFilenamesList():
    extensions = [ ".jpg",".jpeg",'.png','.gif','.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),extensions)

    list_of_fotos.clear()
    for filename in filenames:
        list_of_fotos.addItem(filename)
#///////Работа программы///////
class Imageprocessor():
    def __init__(self):
        self.image = None 
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def saveImage(self):
        path = os.path.join(self.dir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)

    def loadImage(self, dir,filename):
        self.dir = dir
        self.filename = filename
        file_path = os.path.join(dir,filename)
        self.image = Image.open(file_path)
    def showImage(self,path):
        label_win.hide()
        pixmapimage = QPixmap(path)
        w,h = label_win.width(),label_win.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        label_win.setPixmap(pixmapimage)
        label_win.show()
#/////////////////////
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir,self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
#//////////////////
def showchosenImage():
    if list_of_fotos.currentRow() >= 0:
        filename = list_of_fotos.currentItem().text()
        workimage.loadImage(workdir,filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))
        
#\\\\\\\\\\\\\\END///////////////
workimage = Imageprocessor()
list_of_fotos.currentRowChanged.connect(showchosenImage)
btn_folder.clicked.connect(showFilenamesList)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right2.clicked.connect(workimage.do_right)
btn_right.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)
main_win.setLayout(VLayout)
main_win.show()
app.exec_()
