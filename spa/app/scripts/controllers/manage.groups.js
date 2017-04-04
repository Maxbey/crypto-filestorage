'use strict';

angular.module('socialAggregator')
    .controller('ManageGroupsController', function (UserService) {
        var vm = this;
        vm.searchUser = searchUser;

        function searchUser(searchValue) {
            if (!searchValue)
                return [];

            return UserService.searchUser(searchValue);
        }
    });
