var app = angular.module('app', []);


  app.controller("indexController",['$scope', '$http', function($scope,$http){
    $scope.videos = {};
    $scope.getVideoList = function(){
      $http({
        method:'GET',
        url : '/videolist'
      }).success(function(response){
        $scope.videos = response;
      })
    }
    $scope.getVideoList();
  }])

  app.controller("broadcastController",['$scope','$http',function($scope,$http){
    $scope.dataBroadcast = {};
    $scope.sendBroadcast = function (update_data){
      $http({
        method: 'POST',
        url: '/createbroadcast',
        data: JSON.stringify($scope.dataBroadcast),
        headers :  {'Content-Type': 'application/json'}
      }).success(function (data){
        $scope.msg = data
      }).error(function (data){
          $scope.msg = "Please create the event again"
      })
    };
  }]);

  app.controller("loginController",['$scope','$http', '$window', function($scope,$http,$window){
    $scope.loggin = {};
    $scope.send = function (){
      $http({
        method: 'POST',
        url: '/login',
        data: JSON.stringify($scope.loggin),
        headers :  {'Content-Type': 'application/json'} 
      }).success(function (data){
        $scope.msg = data
        $window.location.href = '/createbroadcast';
      }).error(function (data){
          $scope.msg = "User o password wrong"
        })
      }
  }])

  app.controller("dataListController",['$scope','$http','$window',function($scope,$http,$window){
    $scope.events = {}
    $scope.getList = function(){
      $http({
        method: "GET",
        url: "/streamlist"
      }).success(function(response){
        $scope.events = response;
     })
    }

    $scope.startStream = function(streamkey){
      dataSend = {"streamkey" : streamkey}
      $http({
        method: "POST",
        url: "/startstreaming",
        data: dataSend,
        headers :  {'Content-Type': 'application/JSON'} 
      }).success(function (response){
        console.log(response)
        $window.location.href = '/subtitles';

      })
    }
    $scope.getList();
  }]) 

  app.controller("subtitlesController",['$scope','$http',function($scope,$http){
    $scope.subText = {};
    $scope.sendSubtitles = function(){
      $http({
        method: 'POST',
        url: '/subtitles',
        data: JSON.stringify($scope.subText)
      }).success(function (response){
        console.log(response)
        $scope.response = response
      })
    }
  }])