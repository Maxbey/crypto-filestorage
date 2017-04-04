'use strict';

angular.module('socialAggregator')
  .controller('LoginController', function(ToastService, $state, $auth, FormService, ResponseService) {
    var vm = this;

    vm.login = login;
    vm.backendValidationErrors = {};
    vm.resetServerValidation = resetServerValidation;

    function resetServerValidation(formField) {
      FormService.resetServerValidation(formField, 'serverValidation');
    }

    function login(form) {
      $auth.login({
        username: vm.email,
        password: vm.password,
        authy_token: vm.authy_token
      }).then(function(response){
         ToastService.show('You are successfully logged in');
      }, function(response) {
        ToastService.show('Authentication failed');
          vm.backendValidationErrors = ResponseService.parseResponseErrors(response.data);
          FormService.setServerValidation(form, vm.backendValidationErrors, 'serverValidation');
      });
    }
  });
