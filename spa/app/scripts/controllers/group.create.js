'use strict';

angular.module('socialAggregator')
    .controller('GroupCreateController', function (UserService, $state) {
        var vm = this;

        vm.selectedUsers = [];
        vm.selectedPermissions = [];

        vm.userQuery = function(searchValue){
            return UserService.searchUser(searchValue);
        };

        UserService.permissions().then(function(response){
            vm.permissions = response.data;
        });

        vm.createGroup = function(){
            UserService.createGroup(
                vm.groupName,
                vm.selectedUsers,
                vm.selectedPermissions
            ).then(function(){
                $state.go('app.groups');
            });
        };
    });
