import jderobot
import threading
from PIL import Image
import os
import JdeRobot.ImageProviderI.ImageProviderI

class WorkQueue(threading.Thread):
    def __init__(self):
        self.callbacks = []
        threading.Thread.__init__(self)
        

    def run(self):
        if not len(self.callbacks) == 0:
            print(self.callbacks[0])
            self.callbacks[0].execute()
            del self.callbacks[0]
			
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
		if not self.getData():
			self.cb.ice_exception(jderobot.Image.DataNotExistException())
			return
		print(self.imageDescription)
		self.cb.ice_response(self.imageDescription)

	def getData(self):
		if os.path.isfile('./image.jpg'):
			self.imageDescription = jderobot.ImageData()
			self.imageDescription.description = ImageProviderI.getImageDescription(self)
			self.im = Image.open('./image.jpg','r')
			self.im = self.im.convert('RGB')
			self.imRGB = list(im.getdata())
			self.pixelData = []
			for pixeList in self.imRGB:
				for pixel in pixeList:
					self.pixelData.append(pixel)
			self.imageDescription.pixelData = self.pixelData
			return True
		else:
			return False
