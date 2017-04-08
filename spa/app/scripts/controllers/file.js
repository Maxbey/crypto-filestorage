'use strict';

angular.module('socialAggregator')
    .controller('FileController', function (UserService, $stateParams, $window, FormService, ResponseService) {
        var vm = this;

        vm.backendValidationErrors = {};
        vm.resetServerValidation = resetServerValidation;

        vm.downloadLink = false;
        vm.verifySalt = verifySalt;

        UserService.file($stateParams.id).then(function (response) {
            vm.file = response.data;
        });

        function resetServerValidation(formField) {
            FormService.resetServerValidation(formField, 'serverValidation');
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

    });
