'use strict';

angular.module('socialAggregator')
    .controller('GroupsController', function (UserService) {
        var vm = this;

        UserService.allGroups().then(function (response) {
            vm.groups = response.data;
        });

        vm.tableParams = {
            order: 'id',
            page: 1,
            limit: 5
        };

        vm.selected = [];
    });
