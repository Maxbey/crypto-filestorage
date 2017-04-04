'use strict';

angular.module('socialAggregator')
  .factory('AuthenticationService', function($http, $auth, $state) {
    var baseUrl = 'http://api.cryptoapp.dev/api/auth';

    return {
      stateControl: stateControl,
      register: register,
      logout: logout
    };

    function stateControl(event, toState) {
      if (toState.data && toState.data.auth) {
        if (!$auth.isAuthenticated()) {
          event.preventDefault();
          return $state.go('enter.login');
        }
      }
    }

    function register(email, password1, password2, username, cellphone) {
      return $http.post(baseUrl + '/register/', {
        username: username,
        password1: password1,
        password2: password2,
        email: email,
        cellphone: cellphone
      });
    }

    function logout() {
      return $http.post(baseUrl + '/logout/');
    }
  });
