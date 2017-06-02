import sys
from threadFlow import ThreadImage,ThreadDownload
from processVideo import processVideo

if __name__ == '__main__':

	dataFlow = processVideo()
	dataFlow.setURL(sys.argv[1])
	dataFlow.setFileList()

	t1 = ThreadDownload(dataFlow)
	t2 = ThreadImage(dataFlow)
	t1.start()
	t2.start()

	while(True):
		dataFlow.changeName()



