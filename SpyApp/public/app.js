var app = angular.module('app', []);

  //index.html controller
  app.controller("indexController",['$scope', '$http',function($scope,$http,$cookies){
    $scope.setNavbar = "static/navbar.html"
    
    $scope.videos = {};
    //Add iframe element to index.html
    $scope.addVideo = function(video){
      if(video.length > 0){
        var iframe = document.createElement("iframe")
        //Extract iframe src
        console.log(video.substring(video.indexOf('src=') + 5 ,video.indexOf('frameborder') - 2) )
        iframe.src = video.substring(video.indexOf('src=') + 5 ,video.indexOf('frameborder') - 2) 
        var div = document.getElementById("videoContainer");
        div.appendChild(iframe);
      }
    }

    $scope.getVideoList = function(){
      $http({
        method:'GET',
        url : '/videolist'
      }).success(function(response){
        $scope.videos = response.data;
      }).error(function (response){
        $scope.msg = "Can´t show the videos"
      })
    }
    $scope.getVideoList();
  }])

  //createBroadcast.html controller
  app.controller("broadcastController",['$scope','$http',function($scope,$http){
    $scope.dataBroadcast = {};
    $scope.sendBroadcast = function (update_data){
      $scope.msg = ""
      $http({
        method: 'POST',
        url: '/createbroadcast',
        data: JSON.stringify($scope.dataBroadcast),
        headers :  {'Content-Type': 'application/json'}
      }).success(function (response){
        $scope.msg = "Event created"
      }).error(function (response){
          $scope.msg = "Please create the event again"
      })
    };
  }]);

  //login.html controller
  app.controller("loginController",['$scope','$http', '$window', function($scope,$http,$window){
    $scope.loggin = {};
    $scope.send = function (){
      $http({
        method: 'POST',
        url: '/login',
        data: JSON.stringify($scope.loggin),
        headers :  {'Content-Type': 'application/json'} 
      }).success(function (response){
        $scope.msg = response;
        $window.location.href = '/'
      }).error(function (response){
          $scope.msg = "User o password wrong"
      })
      }
  }])

  //stream_list.html controller
  app.controller("dataListController",['$scope','$http','$window',function($scope,$http,$window){
    $scope.events = {}
    $scope.getList = function(){
      $http({
        method: "GET",
        url: "/streamlist"
      }).success(function(response){
        $scope.events = response;
     }).error(function(response){
        $scope.msg = "Can't show video list"   
     })
    }

    $scope.startStream = function(streamkey,quality){
      dataSend = {"streamkey" : streamkey,"quality": quality}
      $http({
        method: "POST",
        url: "/startstreaming",
        data: dataSend,
        headers :  {'Content-Type': 'application/JSON'} 
      }).success(function (response){
        console.log(response)
        $window.location.href = '/subtitles';
      }).error(function(response){
        $scope.msg = "Can't start the event"
      })
    }
    $scope.getList();
  }]) 

  //subtitles.html controller
  app.controller("subtitlesController",['$scope','$http',function($scope,$http){
    $scope.subText = {};
    $scope.sendSubtitles = function(){
      $scope.msg=""
      $http({
        method: 'POST',
        url: '/subtitles',
        data: JSON.stringify($scope.subText)
      }).success(function (response){
        console.log(response)
        $scope.msg = "Subtitles add"
      }).error(function(response){
        $scope.msg  = "Can't add subtitles video"
      })
    }
  }])

  app.controller("logoutController",['$scope','$http', '$window',function($scope,$http,$window){
    $scope.logout = function(){
    $http({
        method: "GET",
        url: "/logout"
      }).success(function(){
        $window.location.href = "/"
    })
  }
  }])