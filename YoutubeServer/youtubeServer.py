import Ice
import sys
import JdeRobot
from PIL import Image
from easyiceconfig import easyiceconfig as EasyIce
from videoTools.processVideo import processVideo
from videoTools.threadFlow import ThreadImage,ThreadDownload,ThreadChangeName
from JdeRobot.ImageProviderI import ImageProviderI,WorkQueue



if __name__== "__main__":

	try:
		ic = EasyIce.initialize(sys.argv)
		prop = ic.getProperties()
		endpoint = prop.getProperty('youtubeServer.Endpoints')
		URL = prop.getProperty('URL')
		liveBroadcast = prop.getProperty('liveBroadcast')
		print(endpoint)
		workQueue = WorkQueue()
		workQueue.setDaemon(True)
		dataFlow = processVideo()
		dataFlow.setURL(URL)
		if liveBroadcast :
			dataFlow.setFileList()

		downloadThread = ThreadDownload(dataFlow)
		imageThread = ThreadImage(dataFlow)
		nameThread = ThreadChangeName(dataFlow)

		downloadThread.start()
		imageThread.start()
		nameThread.start()
		workQueue.start()

		adapter = ic.createObjectAdapterWithEndpoints("youtubeServer",endpoint) #Properties
		object = ImageProviderI(workQueue)
		adapter.add(object, Ice.stringToIdentity("youtubeServer"))
		adapter.activate()
		workQueue.join()
		print('esperar a cierre')
		ic.waitForShutdown()
	except KeyboardInterrupt:
		sys.exit()        

  
