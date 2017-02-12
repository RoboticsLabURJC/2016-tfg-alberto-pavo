import sys
import easyiceconfig as EasyIce
from gui.threadGUI import ThreadGUI
from parallelIce.cameraClient import CameraClient
from gui.cameraWidget import CameraWidget
from PyQt5.QtWidgets import QApplication


import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
    ic = EasyIce.initialize(sys.argv)
    prop = ic.getProperties()
    remoteCamera = CameraClient(ic, "Introrob.Camera", True)
    app = QApplication(sys.argv)
    camera = CameraWidget()
    camera.setCamera(remoteCamera)
    if (len(sys.argv)== 3 and sys.argv[2] == "GUI"):
        camera.setGUI = True
        camera.initUI()
        camera.show()
    else:
        print("For see the GUI, add to command GUI")

    t2 = ThreadGUI(camera)  
    t2.daemon=True
    t2.start()
    
    sys.exit(app.exec_()) 

