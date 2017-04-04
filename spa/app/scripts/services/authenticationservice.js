'use strict';

angular.module('socialAggregator')
  .factory('AuthenticationService', function($http, $auth, $state) {
    return {
      stateControl: stateControl
    };

    function stateControl(event, toState) {
      if (toState.data && toState.data.auth) {
        if (!$auth.isAuthenticated()) {
          event.preventDefault();
          return $state.go('enter.login');
        }
      }
    }
  });
