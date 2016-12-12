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
//server.use("/createbroadcast",security.middleware) //para esta ruta usa seguridad si deja pasar va al get
//server.use("/streams",security.middleware) //para esta ruta usa seguridad si deja pasar va al get 



server.use(express.static(path.join(__dirname, 'public')));

server
	.get('/', function (req, res){
  		res.sendFile(path.join(__dirname + '/public/index.html'));
	})
	.get('/videolist', function (req, res){
  		youtube.retrieveStreamList(req,res,"active")
	})
	.get('/createbroadcast', function (req, res, next) {
  		res.sendFile(path.join(__dirname + '/public/createBroadcast.html'));
	})
	.post('/createbroadcast',function (req, res) {
		youtube.createEvent(req,res);
		
	})
	.get('/login', function (req,res, next){
		res.sendFile(path.join(__dirname + '/public/login.html'));
	})
	.post('/login', function(req,res,next){ 
		security.login(req,res,session,config);
	})
	.get('/streams', function (req,res){
		res.sendFile(path.join(__dirname + '/public/stream_list.html'));
	})
	.get('/streamlist', function (req,res){
		youtube.retrieveStreamList(req,res,"upcoming")
	})
	.post('/startstreaming', function (req,res){
		youtube.startStreaming(req,res)
	})
	.get('/subtitles', function (req,res){
		res.sendFile(path.join(__dirname + '/public/subtitles.html'));
	})
	.post('/subtitles', function (req,res){
		youtube.addSubtitles(req,res)
	})


server.listen(config.server.PORT, function () {
  console.log('Example app listening on port ' + config.server.PORT);
});
