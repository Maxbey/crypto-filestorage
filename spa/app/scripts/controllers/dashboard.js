'use strict';

angular.module('socialAggregator')
  .controller('DashboardController', function(UserService) {
    var vm = this;

    UserService.files().then(function(response){
      vm.files = response.data;
    });
    
  });
