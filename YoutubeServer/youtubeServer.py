import Ice
import sys
import JdeRobot
import config
import comm
from PIL import Image
from easyiceconfig import easyiceconfig as EasyIce
from videoTools.processVideo import processVideo
from videoTools.threadFlow import ThreadImage,ThreadDownload,ThreadChangeName
from JdeRobot.ImageProviderI import ImageProviderI,WorkQueue



if __name__== "__main__":

	try:
		cfg = config.load(sys.argv[1])
		jdrc = comm.init(cfg,"youtubeServer")
		ic = jdrc.getIc()
		endpoint = cfg.getProperty("youtubeServer.ImageSrv.Proxy")
		URL = cfg.getProperty("youtubeServer.ImageSrv.URL")
		liveBroadcast = cfg.getProperty("youtubeServer.ImageSrv.LiveBroadcast")
		print endpoint
		workQueue = WorkQueue()
		workQueue.setDaemon(True)
		dataFlow = processVideo()
		dataFlow.setURL(URL)
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
		print 'esperar a cierre'
		ic.waitForShutdown()
	except KeyboardInterrupt:
		sys.exit()        
