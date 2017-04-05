'use strict';

angular.module('socialAggregator')
  .factory('UserService', function ($http) {
    var baseUrl = 'http://api.cryptoapp.dev/api/auth';

    return {
      searchUser: searchUser,
      allGroups: allGroups,
      updateUserGroups: updateUserGroups
    };

    function searchUser(username) {
      var url = baseUrl + '/user/search/';

      return $http.post(url, {
            username: username
        }).then(function(response) {
            return response.data;
        });
    }

    function allGroups() {
      var url = baseUrl + '/group/';

      return $http.get(url);
    }

    function updateUserGroups(user, groups) {
      var url = baseUrl + '/user/group/';

      return $http.post(url, {
        user: user.id,
        groups: groups
      });
    }

  });
