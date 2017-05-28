import Ice
import sys,traceback,os
import threading
from PIL import Image
from easyiceconfig import easyiceconfig as EasyIce
from videoTools.processVideo import processVideo
from videoTools.threadFlow import ThreadImage,ThreadDownload
from datetime import datetime
import jderobot


class WorkQueue(threading.Thread):
    def __init__(self):
        self.callbacks = []
        threading.Thread.__init__(self)
       

    def run(self):
        print("run")
        if not len(self.callbacks) == 0:
            print("Ejecutando tarea....")
            print(self.callbacks[0])
            self.callbacks[0].execute()
            del self.callbacks[0]
        else:
            print("No hay tareas en la cola")
           
    def add(self, job):
        self.callbacks.append(job)
        print("Tarea Añadida")
        self.run()
       

class Job(object):
   
    def __init__(self,cb,formato):
        self.cb = cb
        self.format = formato
        self.imageDescription = jderobot.ImageData()
   
    def execute(self):
        print("Ejecutando....")
        if not self.getData():
            self.cb.ice_exception(jderobot.Image.DataNotExistException())
            return
        print(self.imageDescription)
        self.cb.ice_response(self.imageDescription)
        print("Tarea ejecutada")

    def getData(self):
        print("Obteniendo datos...")
        if os.path.isfile('./image.jpg'):
            self.imageDescription = jderobot.ImageData()
            self.image= Image.open('./image.jpg')
            self.imageDescription.description = ImageProviderI.getImageDescription(self)
            self.imageDescription.pixeldata = self.image.bits
            return True
        else:
            return False


class ImageProviderI(jderobot.Camera):

  def __init__(self,workQueue):
    self.workQueue = workQueue

  def getCameraDescription(self):
    return 0

  def setCameraDescription(description):
    return 0

  def startCameraStreaming(self):
    return ''
   
  def stopCameraStreaming(self,current=None):
    print('entraaa')

  def reset(self):
    print('---')

  def getImageDescription(self,current=None):

    self.imageData = jderobot.ImageDescription()
    print('getImageDescription')   
    if os.path.isfile('./image.jpg'):
      self.image= Image.open('./image.jpg')
      self.imageData.width = self.image.width
      self.imageData.height = self.image.height
      self.format = 'RGB'
      return self.imageData

  def getImageData_async(self,cb,formato,curren=None):
    print ("imageData")
    job = Job(cb,formato)
    return self.workQueue.add(job)
       

if __name__== "__main__":
    print('Server Started')
    ic = EasyIce.initialize(sys.argv)
    prop = ic.getProperties()
    endpoint = prop.getProperty('youtubeServer.Endpoints')
    workQueue = WorkQueue()
    workQueue.setDaemon(True)
    workQueue.start()
    adapter = ic.createObjectAdapterWithEndpoints("youtubeServer",endpoint) #Properties
    object = ImageProviderI(workQueue)
    adapter.add(object, Ice.stringToIdentity("youtubeServer"))
    adapter.activate()
    workQueue.join()
    ic.waitForShutdown()
   




   

  