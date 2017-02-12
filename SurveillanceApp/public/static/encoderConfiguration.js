var config = new Map();

config.set("240p",{"resolution":"320x240","bitrate":"500k"})
config.set("360p",{"resolution":"640x360","bitrate":"900k"})
config.set("480p",{"resolution":"854x480","bitrate":"1700k"})
config.set("720p",{"resolution":"1280x720","bitrate":"3500k"})
config.set("1080p",{"resolution":"1920x1080","bitrate":"5000k"})


exports.getConfig = function(quality){
	return config.get(quality)
}