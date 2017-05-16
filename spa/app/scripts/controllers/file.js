'use strict';

angular.module('socialAggregator')
    .controller('FileController', function (UserService, $stateParams, $window, FormService, ResponseService, ToastService) {
        var vm = this;

        vm.backendValidationErrors = {};
        vm.resetServerValidation = resetServerValidation;

        vm.downloadLink = false;
        vm.verifySalt = verifySalt;

        vm.selectedGroups = [];

        UserService.file($stateParams.id).then(function (response) {
            vm.file = response.data;
            UserService.allGroups().then(function(response){
                vm.groups = response.data;
                fetchGroupModels(vm.file);
            });
        });

        function resetServerValidation(formField) {
            FormService.resetServerValidation(formField, 'serverValidation');
        }

        function findById(collection, id) {
            for (var index in collection){
                if (collection[index].id == id)
                    return collection[index];
            }

            return false;
        }

        function fetchGroupModels(file) {

            for (var index in file.groups) {
                var group = findById(vm.groups, file.groups[index].id);

                if (group)
                    vm.selectedGroups.push(group);
            }
        }

        function verifySalt(form) {
            UserService.verifySalt($stateParams.id, vm.salt).then(function (response) {
                var blob = new Blob([response.data.file], { type: 'text/plain' });
                var url = $window.URL;
                vm.downloadLink = url.createObjectURL(blob);
            }, function (response) {
                vm.downloadLink = false;
                vm.backendValidationErrors = ResponseService.parseResponseErrors(response.data);
                FormService.setServerValidation(form, vm.backendValidationErrors, 'serverValidation');
            });
        }

        vm.updateFileGroups = function(){
            var ids = [];

            for (var index in vm.selectedGroups)
                ids.push(vm.selectedGroups[index].id);

            UserService.updateFileGroups(vm.file.id, ids).then(function() {
                ToastService.show('Groups updated');
            }, function() {
                ToastService.show('Groups updated');
            });
        };

    });
