var express = require('express');
var path = require('path');
var config = require('./private/config.json')
var server = express();
var session = require('express-session');
var security = require('./public/security.js');
var server = express();
var bodyParser=require("body-parser");
var youtube = require('./public/youtube-controller')


server.use(bodyParser.json());
server.use(session({secret: '53CR37CL13N7',resave: true,saveUninitialized: true}));

//Middleware
server.use("/admin",security.middleware) 


server.use(express.static(path.join(__dirname, 'public')));

server
	.get('/', function (req, res){
  		res.sendFile(path.join(__dirname + '/public/index.html'));
	})
	.get('/videolist', function (req, res){
  		youtube.retrieveStreamList(req,res,"active",true)
	})
	.get('/admin',function(req,res){
		res.sendFile(path.join(__dirname + '/public/admin.html'));
	})
	.get('/login', function (req,res){
		res.sendFile(path.join(__dirname + '/public/login.html'));
	})
	.get('/logout',function(req,res){
		security.logout(req,res)
	})
	.post('/start', function(req,res){
		console.log("start")
		youtube.startStream(req,res,config.imagePath)
	})
	.post('/login', function(req,res,next){ 
		security.login(req,res,session,config);
	})
	.post('/stop',function (req,res){
		youtube.stopStream(req,res)
	})
	.post('/subtitles', function (req,res){
		youtube.addSubtitles(req,res)
	})
	


server.listen(config.server.PORT, function () {
  console.log('App listening on port ' + config.server.PORT);
});
