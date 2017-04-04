'use strict';

angular.module('socialAggregator')
  .controller('HeaderLoggedController', function($auth, $state, AuthenticationService) {
    var vm = this;

    vm.logout = logout;

    function logout() {
      $auth.logout();
      AuthenticationService.logout();
      $state.go('enter.login');
    }
  });
