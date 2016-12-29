var sess;

exports.middleware = function(req,res,next){
  sess = req.session
  if(sess.auth){
      next(); //if log ok ==> continue
  } else{
     console.log("Incorrect User")
     res.redirect("/login")

  }
}

exports.login = function(req,res,session,config){  
  
  if(req.body.user == config.admin.name && req.body.password == config.admin.password){
     sess = req.session;
     console.log("Right User : session started")
     sess.auth = "true";
     res.end("Right user")
  } else{
    res.status(400).end("User or Password Error");
  }
}

exports.logout = function(req,res){
  req.session.destroy();
  res.redirect("/login")
}