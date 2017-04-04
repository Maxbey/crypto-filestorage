'use strict';

angular.module('socialAggregator')
  .factory('UserService', function ($http) {
    return {
      searchUser: searchUser
    };

    function searchUser(username) {
      var url = 'http://api.cryptoapp.dev/api/auth/user/search/'
      return $http.post(url, {
            username: username
        }).then(function(response) {
            return response.data;
        });
    }

  });
