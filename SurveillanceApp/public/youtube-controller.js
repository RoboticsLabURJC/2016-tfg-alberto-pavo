var spawn = require('child_process').spawn;
var fs=require('fs');
var encoder = require("./static/encoderConfiguration.js")


exports.createEvent =  function(req,res){

	arg = JSON.stringify(req.body)

	var process = spawn('python',['./public/python/createEvent.py', '--dataBr' , arg]);
	processOutput(res,process);
}

exports.retrieveStreamList =  function(req,res,status){

	var process = spawn('python',['./public/python/streamList.py', '--status' , status]);
	processOutput(res,process);
}

exports.startStreaming = function(req,res){
	arg = req.body
	//return a map with encoder configuration
	res.end("Broadcast Started")
	var encoderSettings = encoder.getConfig(arg.quality)
	var process = spawn('python',['./public/python/startStream.py', arg.streamkey,encoderSettings.resolution,encoderSettings.bitrate]);
}

exports.addSubtitles = function(req,res){
	msg = req.body.subtitles
	fs.writeFile('./public/static/subtitles.txt', msg ,  function(err) {
   		if (err) {
    		res.status(500).end();
    		return;
   		}
   		res.end("Write Succesfull")
	})	
}

exports.stopStream = function(req,res){
	console.log(req.body)
	arg = req.body.brId
	console.log("----------------------------" + arg)
	var process = spawn('python',['./public/python/stopEvent.py', '--brID' , arg]);
	processOutput(res,process);

}


function processOutput(res,process){

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
  	 	  res.end(py_data)
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