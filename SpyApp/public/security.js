var sess;

exports.middleware = function(req,res,next){
  sess = req.session
  if(sess.auth){ //server.use(/createBroadcast, function())
      console.log("usuario valido")
      next(); //si esta loggeado le dejo pasar
  } else{
     console.log("no valido")
     res.redirect("/login") //si no esta loggeado le redirijo al login

  }
}

exports.login = function(req,res,session,config){  
  console.log(config.admin.name + " " + config.admin.password)
  if(req.body.user == config.admin.name && req.body.password == config.admin.password){
     sess = req.session;
     sess.auth = "true";
     res.end("usuario valido")
  } else{
    res.end("User or Password Error");
  }
}