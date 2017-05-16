'use strict';

angular.module('socialAggregator')
  .factory('UserService', function ($http) {
    var baseUrl = 'http://api.cryptoapp.dev/api/auth';

    return {
      searchUser: searchUser,
      allGroups: allGroups,
      files: files,
      file: file,
      permissions: permissions,
      verifySalt: verifySalt,
      createGroup: createGroup,
      updateFileGroups: updateFileGroups
    };

    function getIds(collection){
      var ids = [];

      for (var index in collection)
        ids.push(collection[index].id);
      
      return ids;
    }

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

    function permissions() {
      var url = baseUrl + '/permission/';

      return $http.get(url);
    }

    function createGroup(name, users, permissions) {
      var url = baseUrl + '/group/';

      return $http.post(url, {
        name: name,
        user_set: getIds(users),
        permissions: getIds(permissions)
      });
    }

    function files() {
      var url = 'http://api.cryptoapp.dev/api/storage/file/';

      return $http.get(url);
    }

    function file(id) {
      var url = 'http://api.cryptoapp.dev/api/storage/file/' + id + '/';

      return $http.get(url);
    }

    function updateFileGroups(id, groups) {
      var url = 'http://api.cryptoapp.dev/api/storage/file/group/' + id + '/';

      return $http.put(url, {
        groups: groups
      });
    }

    function verifySalt(fileId, salt){
      var url = 'http://api.cryptoapp.dev/api/storage/decrypt/';

      return $http.post(url, {
        file: fileId,
        salt: salt
      });
    }

  });
