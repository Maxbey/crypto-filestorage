'use strict';

angular.module('socialAggregator')
  .factory('UserService', function ($http) {
    var baseUrl = 'http://api.cryptoapp.dev/api/auth';

    return {
      searchUser: searchUser,
      allGroups: allGroups,
      updateUserGroups: updateUserGroups,
      files: files,
      file: file,
      verifySalt: verifySalt
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

    function files() {
      var url = 'http://api.cryptoapp.dev/api/storage/files/';

      return $http.get(url);
    }

    function file(id) {
      var url = 'http://api.cryptoapp.dev/api/storage/files/' + id + '/';

      return $http.get(url);
    }

    function verifySalt(fileId, salt){
      var url = 'http://api.cryptoapp.dev/api/storage/decrypt/';

      return $http.post(url, {
        file: fileId,
        salt: salt
      });
    }

  });
