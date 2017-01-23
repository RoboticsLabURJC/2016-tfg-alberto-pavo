#
#  Copyright (C) 1997-2015 JDE Developers Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/.
#  Authors :
#       Alberto Martin Florido <almartinflorido@gmail.com>
#
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QPushButton,QWidget, QLabel
from gui.communicator import Communicator
from PIL import Image
import os

class CameraWidget(QWidget):
    IMAGE_COLS_MAX=640
    IMAGE_ROWS_MAX=360    
    LINX=0.3
    LINY=0.3
    LINZ=0.8
    ANGZ=1.0
    ANGY=0.0
    ANGX=0.0    
    
    imageUpdate=pyqtSignal()
    updGUI=pyqtSignal()

    def __init__(self,parent = None):      
        super(CameraWidget, self).__init__(parent)
        self.imageUpdate.connect(self.updateImage)
        self.updGUI.connect(self.updateGUI)
        self.initUI()
        
    def initUI(self):
        
        self.setMinimumSize(680,500)
        self.setMaximumSize(680,500)
        
        self.setWindowTitle("Camera")
        
        self.imgLabel=QLabel(self)
        self.imgLabel.resize(640,360)
        self.imgLabel.move(10,5)
        self.imgLabel.show()

    def setCamera(self,camera):
        self.camera = camera

    def getCamera(self):
        return self.camera

    def updateGUI(self):
        self.imageUpdate.emit()
        
    def updateImage(self):

        img = self.getCamera().getImage()
        if img is not None:
            im = Image.fromarray(img)
            im.save("temp.jpg")
            os.rename("temp.jpg","imagen.jpg")
            image = QImage(img.data, img.shape[1], img.shape[0], img.shape[1]*img.shape[2], QImage.Format_RGB888);
        
            if img.shape[1]==self.IMAGE_COLS_MAX:
                x=20
            else:
                x=(self.IMAGE_COLS_MAX+20)/2-(img.shape[1]/2)
            if img.shape[0]==self.IMAGE_ROWS_MAX:
                y=40
            else:
                y=(self.IMAGE_ROWS_MAX+40)/2-(img.shape[0]/2)
            
            size=QSize(img.shape[1],img.shape[0])
            self.imgLabel.move(x,y)
            self.imgLabel.resize(size)
            self.imgLabel.setPixmap(QPixmap.fromImage(image))
        
