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
        threading.Thread.__init__(self)
        self._callbacks = []
        self._done = False
        self._cond = threading.Condition()

    def run(self):
        with self._cond:
            while not self._done:
                if len(self._callbacks) == 0:
                    print('No hay tareas')
                    self._cond.wait()

                if not len(self._callbacks) == 0:

                    if not self._done:
                        print ("GetImage")
                        if os.path.isfile('./image.jpg'):
                            self.imageDescription = jderobot.ImageData()
                            self.image= Image.open('./image.jpg')
                            self.imageDescription.description = getImageDescription()
                            self.imageDescription.pixeldata = image.bits
                            return self.imageDescription
                        self._callbacks[0].future.set_result(None)
                        del self._callbacks[0]

            for i in range(0, len(self._callbacks)):
                self._callbacks[i].future.set_exception(Demo.RequestCanceledException())

    def add(self, delay):
        future = Ice.Future()
        with self._cond:
            if not self._done:
                entry = CallbackEntry(future, delay)
                if len(self._callbacks) == 0:
                    self._cond.notify()
                self._callbacks.append(entry)
            else:
               future.set_exception(Demo.RequestCanceledException())
        return future

    def destroy(self):
        with self._cond:
            self._done = True
            self._cond.notify()



class ImageProviderI(jderobot.Camera):

  def getCameraDescription(self):
    return 0

  def setCameraDescription(description):
    return 0

  def startCameraStreaming(self):
    return ''
	
  def stopCameraStreaming(self,current=None):
    print('--------')

  def reset(self):
    print('---')

  def getImageDescription(self,current=None):

    self.imageData = jderobot.ImageDescription()
    print('getImageDescription')    
    if os.path.isfile('./image.jpg'):
      self.image= Image.open('./image.jpg')
      self.imageData.width = self.image.width
      self.imageData.height = self.image.heigth
      self.format = 'RGB'
      return self.imageData

  def getImageData(self,format,current=None):
    print("Entra")
    return self._workQueue.add(format)
		

try:
	print('Server Started')
	ic = EasyIce.initialize(sys.argv)
	prop = ic.getProperties()
	endpoint = prop.getProperty('youtubeServer.Endpoints')
	workQueue = WorkQueue()
	workQueue.start()
	adapter = ic.createObjectAdapterWithEndpoints("youtubeServer",endpoint) #Properties
	object = ImageProviderI()
	adapter.add(object, Ice.stringToIdentity("youtubeServer"))
	adapter.activate()
	ic.waitForShutdown()
	self._workQueue.join()

except:
	traceback.print_exc()
	status= 1

if(ic):
	try:
		ic.destroy()
	except:
		traceback.print_exc()
		status = 1

sys.exit(status)


	

  
