from PyQt6.QtWidgets import QApplication, QFileDialog, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QInputDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
from PIL import Image, ImageEnhance
import shutil

class ImageEditor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.image_path = None
        self.mod_dir = 'Modified/'
        self.data_dir = 'appdata/'
    def show_image(self, path):
        l1.hide()
        pixmapimage = QPixmap(path)
        w, h = l1.width(), l1.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio)
        l1.setPixmap(pixmapimage)
        l1.show()

def chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files,extentions):
    results = []
    for file in files:
        for ext in extentions:
            if file.endswith(ext):
                results.append(file)
    return results

def showFilenameList():
    try:
        global extentions
        global filenames
        extentions = [".jpg",".png", ".gif", ".bmp", ".jpeg"]
        chooseworkdir()
        filenames = filter(os.listdir(workdir),extentions)
        imagenames.clear()
        for file in filenames:
            imagenames.addItem(file)
    except:
        pass

def leftf():
    try:
        global filename
        global image
        image.image = image.image.transpose(Image.ROTATE_90)
        saveappdata()
        image.show_image(appdatadir)
    except:
        pass

def rightf():
    try:
        global filename
        global image
        image.image = image.image.transpose(Image.ROTATE_270)
        saveappdata()
        image.show_image(appdatadir)
    except:
        pass

def mirrorf():
    try:
        global filename
        global image
        image.image = image.image.transpose(Image.FLIP_LEFT_RIGHT)
        saveappdata()
        image.show_image(appdatadir)
    except:
        pass

def sharpf():
    try:
        global filename 
        global image   
        image.image = ImageEnhance.Contrast(image.image)
        image.image = image.image.enhance(1.5)
        saveappdata()
        image.show_image(appdatadir)
    except:
        pass

def bwf():
    try:
        global filename
        global image
        image.image = image.image.convert('L')
        saveappdata()
        image.show_image(appdatadir)
    except:
        pass

def showChosenImage():
    try:
        global filename
        global image
        filename = filenames[imagenames.currentRow()]
        image = ImageEditor()
        image.image_path = os.path.join(workdir, filename)       
        image.show_image(image.image_path)
        image.image = Image.open(image.image_path)
    except:
        pass

def saveappdata():
    try:
        global counter
        global appdatadir
        global appdatafiledir
        global image
        path = os.path.join(workdir, image.data_dir)
        if not(os.path.exists(path)) and not (os.path.isdir(path)):
            os.mkdir(path)
        imgname = 'modified' + str(counter)
        for ext in extentions:
            if filename.endswith(ext):
                imgname += ext
        appdatadir = os.path.join(path, imgname)
        appdatafiledir = path    
        image.image.save(appdatadir)
        counter += 1
    except:
        pass

def save():
    try:
        global image
        global workdir
        global filenames
        path = os.path.join(workdir, image.mod_dir)
        if not(os.path.exists(path)) and not (os.path.isdir(path)):
            os.mkdir(path)
        imgname, ok = QInputDialog.getText(w, "Save image", "Image name:")
        if ok:
            for ext in extentions:
                if filename.endswith(ext):
                    imgname += ext
            image_path = os.path.join(path, imgname)
            image.image.save(image_path)
            workdir = path
            l1.setText('')
            filenames = filter(os.listdir(workdir),extentions)
            imagenames.clear()
            for file in filenames:
                imagenames.addItem(file)
            shutil.rmtree(appdatafiledir)
    except:
        pass

app = QApplication([])
w = QWidget()
w.setWindowTitle("Image Editor")
w.resize(500, 500)
pb1 = QPushButton("Folder")
counter = 0
imagenames = QListWidget()
l1 = QLabel("")
pb2 = QPushButton("Left")
pb3 = QPushButton("Right")
pb4 = QPushButton("Mirror")
pb5 = QPushButton("Sharpness")
pb6 = QPushButton("B/W")
pb7 = QPushButton('Save')
lineofpushbuttons = [pb2, pb3, pb4, pb5, pb6]
lv1 = QVBoxLayout()
lv2 = QVBoxLayout()
lh1 = QHBoxLayout()
lh2 = QHBoxLayout()
lh3 = QHBoxLayout()
lh3.addWidget(pb1)
lh3.addWidget(pb7)
lv1.addLayout(lh3)
lv1.addWidget(imagenames)
for i in lineofpushbuttons:
    lh1.addWidget(i)
lv2.addWidget(l1)
lv2.addLayout(lh1)
lh2.addLayout(lv1)
lh2.addLayout(lv2)
w.setLayout(lh2)
w.show()
pb1.clicked.connect(showFilenameList)
pb2.clicked.connect(leftf)
pb3.clicked.connect(rightf)
pb4.clicked.connect(mirrorf)
pb5.clicked.connect(sharpf)
pb6.clicked.connect(bwf)
pb7.clicked.connect(save)
imagenames.currentRowChanged.connect(showChosenImage)
app.exec()