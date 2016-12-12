var spawn = require('child_process').spawn;
var fs=require('fs');


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
	var process = spawn('python',['./public/python/startStream.py', arg.streamkey]);
	processOutput(res,process);
}

exports.addSubtitles = function(req,res){
	msg = req.body.subtitles
	fs.writeFile('./public/static/subtitles.txt', msg ,  function(err) {
   		if (err) {
    		res.end("ERROR");
    		return;
   		}
   		res.end("Write Succesfull")
	})	
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
  	 		res.end(py_data)
		}	
	})

	process.stderr.on("data", function(data){
  		py_err += data;
	})

	process.stderr.on("end",function(){

		if(typeof py_err !== 'undefined'){
			res.end("ERROR")
  			console.log("Python Error: " + py_err)
		}	
	})
}


