var spawn = require('child_process').spawn;
var fs=require('fs');
var encoder = require("./static/encoderConfiguration.js")
var data;
var brID;


exports.retrieveStreamList =  function(req,res,status,send){
	var process = spawn('python',['./public/python/streamList.py', '--status' , status]);
	processOutput(res,process,send);
}

exports.startStream = function(req,res,imagePath){
	arg = req.body
	//return a map with encoder configuration
	res.end("Event Started")
	var encoderSettings = encoder.getConfig(arg.format)
	var process = spawn('python',['./public/python/startStream.py',imagePath ,arg.stream_key,encoderSettings.resolution,encoderSettings.bitrate]);
processOutput(res,process,false);
}

exports.addSubtitles = function(req,res){
	msg = req.body.subtitles
	var writeStream = fs.createWriteStream("./public/static/tempSubtitles.txt");
	writeStream.write(msg);
	writeStream.end();
	fs.rename('./public/static/tempSubtitles.txt', './public/static/subtitles.txt', function(err) {
    if (err) {
    		res.status(500).end();
    		return;
   		}
   		res.end("Write Succesfull")
});	
}

exports.stopStream = function(req,res){
	brID = req.body.brID
	var process = spawn('python',['./public/python/stopEvent.py', '--brID' , brID]);
	processOutput(res,process,true);
}


function processOutput(res,process,send){

	var py_data;
	var py_err;
	
	process.stdout.on("data",function(data){
  			py_data += data;//obtenemos el string
	})
	
	process.stdout.on("end",function(){
	if(typeof py_data !== "undefined"){
      py_data = py_data.substring(9);
      console.log(py_data)
      if(py_data.localeCompare("ERROR") == 1){
        res.status(500).end();
      }else{
		  if (send){
			res.end(py_data)
		  }else{
				brID = py_data;
		  }
  	 	  
      }
		}	
	})

	process.stderr.on("data", function(data){
  		py_err += data;
	})

	process.stderr.on("end",function(){
    
		if(typeof py_err !== 'undefined'){
			res.status(500).end()
  			console.log("Python Error: " + py_err)
		}	
	})
}
