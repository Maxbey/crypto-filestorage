'use strict';

angular.module('socialAggregator')
  .controller('HeaderLoggedController', function($auth, $state) {
    var vm = this;

    vm.logout = logout;

    function logout() {
      AuthenticationService.logout();
      $state.go('enter.login');
    }
  });
