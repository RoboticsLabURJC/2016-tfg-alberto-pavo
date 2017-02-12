//meter modal service en html http://jsfiddle.net/dwmkerr/8MVLJ/
//http://stackoverflow.com/questions/35028596/angular-js-return-data-from-service-and-http-callback-method retunr

var app = angular.module('app', ['ui.bootstrap']);
	
  /*******************************************
    Youtube Service for to get active events
  ******************************************/
  
	var videoData = {"response":" "}
	app.service("getVideoList",['$http',function($http){
		this.activeVideos = function(){
			 return $http({
					method:'GET',
					url : '/videolist'
				}).then(
          function successCallback(response){
  					if(response.data.data.length == 0){
  						 return "No avalaibles events now"
  					}else{
  						videoData = response.data.data;
              return videoData;
  					}
            
  				},function errorCallback(response){
  					data.response =  "Can´t show the videos"
            return videoData;
  				})
        }	
      }])

  
  /************************************************************
    Index.html Controller
  *************************************************************/
  app.controller("indexController",['$scope', '$http','$sce','getVideoList',function($scope,$http,$sce,getVideoList){
    $scope.videos = {};
    //Add iframe element to index.html
    $scope.addVideo = function(video){
      if(video.length > 0){
        //Extract iframe src
        src = video.substring(video.indexOf('embed') + 6 ,video.indexOf('?'))
        //iframe.src = ("https://www.youtube.com/embed/watch?v=EyUa9FIzxH0&feature=youtu.be?autoplay=1&livemonitor=1") 
        return $sce.trustAsResourceUrl("https://www.youtube.com/embed/" + src)
      }
    }

    $scope.getVideoActive = function(){
      getVideoList.activeVideos().then(function success(response){
  			if(typeof(response) !== "string" && typeof(response) !== "undefined"){
  				$scope.videos = response;
  			}else{
  				$scope.msg = response;
  			}
      })
    }
      $scope.getVideoActive();
  }])


  /************************************************************
    login.html Controller
  *************************************************************/
  app.controller("loginController",['$scope','$http', '$window',function($scope,$http,$window){
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

  
  /************************************************************
    Data Controller of admin.html 
  *************************************************************/
  app.controller("dataController",['$scope','$http','$window', 'getVideoList','$modal'
    ,function($scope,$http,$window,getVideoList,$modal){
	$scope.data = {};
	$scope.videos = {};
  $scope.stopMsg = ""
  $scope.sendData = function(){
		if(typeof($scope.data.stream_key) == 'undefined' ){
			$scope.msg = "The stream key is necessary"
		}else{
			$http({
				method: "POST",
				url: "/start",
				data: JSON.stringify($scope.data),
				headers :  {'Content-Type': 'application/JSON'} 
			}).success(function (response){
				$scope.msg = "Event Started"
				$("#start").prop( "disabled", true );
			}).error(function(response){
				$scope.msg = "Can't start the event"
			})
		}
		}
	
  $scope.openModal = function(){
    var modalInstance = $modal.open({
      templateUrl: 'stopModal.html',
      controller: modalStopController,
      resolve: {
        videos: function () {
          return $scope.videos;
        }
      }
    })

    modalInstance.result.then(function (brID) {
      dataSend = {"brID" : brID}
      $http({
        method: "POST",
        url: "/stop",
        data: dataSend,
        headers :  {'Content-Type': 'application/JSON'} 
      }).success(function (response){
        $scope.msg = "Event Stoped"
        $("#start").prop( "disabled", false );
      }).error(function(response){
        $scope.msg = "Can't start the event"
      })
    })
  }

	$scope.getVideoActive = function(){
      getVideoList.activeVideos().then(function success(response){
        if(typeof(response) !== "string" && typeof(response) !== "undefined"){
          $scope.videos = response;
        }else{
          $scope.stopMsg = response;
        }
        $scope.openModal()
      })
      
    }
	
}]) 


  /************************************************************
    Modal Controller 
  *************************************************************/


  var modalStopController = function($scope,$modalInstance,videos){
    $scope.videos = videos;
  /*$scope.brID = {
      brID :videos[0].broadcastID
    } */

    $scope.stop = function(brID){
      $modalInstance.close(brID)
    }
    $scope.cancel = function () {
      $modalInstance.dismiss('cancel');
    };
  }

  /************************************************************
    Subtitles of admin.html controller 
  *************************************************************/  
  app.controller("subtitlesController",['$scope','$http',function($scope,$http){
    $scope.subText = {};
    $scope.sendSubtitles = function(){
      $scope.msg=""
      console.log($scope.subText.subtitles)
      if(typeof($scope.subText.subtitles) == 'undefined' || $scope.subText.subtitles == ""){
        $scope.subText = {"subtitles": "        "} //if ffmpeg receive empty file it will fail
      }
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
