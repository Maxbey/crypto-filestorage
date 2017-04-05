'use strict';

angular.module('socialAggregator')
    .controller('ManageGroupsController', function (UserService, ToastService) {
        var vm = this;
        vm.searchUser = searchUser;
        vm.avaliableGroups = [];
        vm.selectedGroups = [];

        vm.updateUserGroups = updateUserGroups;
        vm.getUserGroups = getUserGroups;

        UserService.allGroups().then(function (response) {
            vm.avaliableGroups = response.data;
        });

        function searchUser(searchValue) {
            if (!searchValue)
                return [];

            return UserService.searchUser(searchValue);
        }

        function updateUserGroups() {
            var toUpdateIds = [];

            for (var index in vm.selectedGroups)
                toUpdateIds.push(vm.selectedGroups[index].id);


            UserService.updateUserGroups(vm.selectedUser, toUpdateIds).then(function(response){
                ToastService.show('Groups updated');
            });
        }

        function prepareUserGroups(ids, avaliableGroups) {
            var groups = [];

            for (var index in avaliableGroups) {
                if (ids.indexOf(avaliableGroups[index].id) !== -1)
                    groups.push(avaliableGroups[index]);
            }

            return groups;
        }

        function getUserGroups(user) {
            if (!user)
                return;
            vm.selectedGroups = prepareUserGroups(user.groups, vm.avaliableGroups);
        }
    });
