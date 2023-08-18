from PyQt6.QtWidgets import QApplication, QFileDialog, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QInputDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
from PIL import Image, ImageEnhance, ImageFilter
import shutil

class ImageEditor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.image_path = None
        self.mod_dir = 'Modified/'
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

def imagefilterfunction(filter):
    try:
        global filename
        global image
        image.image = image.image.filter(filter)
        saveappdata()
        image.show_image(appdatadir)
    except:
        pass 

def imagetransposefunction(rotation):
    try:
        global filename
        global image
        image.image = image.image.transpose(rotation)
        saveappdata()
        image.show_image(appdatadir)
    except:
        pass

def leftf():
    imagetransposefunction(Image.ROTATE_90)

def rightf():
    imagetransposefunction(Image.ROTATE_270)

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

def blurfilter():
    imagefilterfunction(ImageFilter.BLUR)

def contour():
    imagefilterfunction(ImageFilter.CONTOUR)

def detail():
    imagefilterfunction(ImageFilter.DETAIL)

def enhance_edge():
    imagefilterfunction(ImageFilter.EDGE_ENHANCE)

def enhance_edge_plus():
    imagefilterfunction(ImageFilter.EDGE_ENHANCE_MORE)

def emboss():
    imagefilterfunction(ImageFilter.EMBOSS)

def find_edges():
    imagefilterfunction(ImageFilter.FIND_EDGES)

def smoothen():
    imagefilterfunction(ImageFilter.SMOOTH)

def smoothenmore():
    imagefilterfunction(ImageFilter.SMOOTH_MORE)

def sharpen():
    imagefilterfunction(ImageFilter.SHARPEN)

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
        path = os.path.join('appdata/')
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
            filenames = filter(os.listdir(workdir), extentions)
            imagenames.clear()
            for file in filenames:
                imagenames.addItem(file)
            shutil.rmtree(appdatafiledir)
    except:
        pass

def delete():
    try:
        global image
        global workdir
        global filenames
        global imagenames
        l1.clear()
        image = None
        nameoffiletoremove = os.path.join(workdir, filenames[imagenames.currentRow()])
        filenames.remove(filenames[imagenames.currentRow()])
        imagenames.takeItem(imagenames.currentRow())
        if len(filenames) == 0:
            shutil.rmtree(workdir)
        else:
            os.remove(nameoffiletoremove)
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
pb8 = QPushButton('Blur')
pb9 = QPushButton("Contour")
pb10 = QPushButton('Enhance edges')
pb11 = QPushButton("Enhance edges +")
pb12 = QPushButton('Emboss')
pb13 = QPushButton('Find edges')
pb14 = QPushButton('Smoothen')
pb15 = QPushButton('Smoothen +')
pb16 = QPushButton('Delete')
lineofpushbuttons = [pb2, pb3, pb4, pb5, pb6, pb8, pb9]
line2ofpushbuttons = [pb10, pb11, pb12, pb13, pb14, pb15]
lv1 = QVBoxLayout()
lv2 = QVBoxLayout()
lh1 = QHBoxLayout()
lh2 = QHBoxLayout()
lh3 = QHBoxLayout()
lh4 = QHBoxLayout()
lh3.addWidget(pb1)
lh3.addWidget(pb7)
lh3.addWidget(pb16)
lv1.addLayout(lh3)
lv1.addWidget(imagenames)
for i in lineofpushbuttons:
    lh1.addWidget(i)
for i in line2ofpushbuttons:
    lh4.addWidget(i)
lv2.addWidget(l1)
lv2.addLayout(lh1)
lv2.addLayout(lh4)
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
pb8.clicked.connect(blurfilter)
pb9.clicked.connect(contour)
pb10.clicked.connect(enhance_edge)
pb11.clicked.connect(enhance_edge_plus)
pb12.clicked.connect(emboss)
pb13.clicked.connect(find_edges)
pb14.clicked.connect(smoothen)
pb15.clicked.connect(smoothenmore)
pb16.clicked.connect(delete)
imagenames.currentRowChanged.connect(showChosenImage)
app.exec()
try:
    shutil.rmtree(appdatafiledir)
except:
    pass