'use strict';

angular.module('socialAggregator')
    .controller('UploadController', function ($scope, $auth) {
        var vm = this;

        vm.dropzoneConfig = {
            parallelUploads: 10,
            maxFileSize: 10,
            url: 'http://api.cryptoapp.dev/api/storage/upload/',
            headers: {
                Authorization: 'Token ' + $auth.getToken()
            }
        };

        vm.preUpload = function (file, xhr, formData) {
            formData.append('salt', vm.salt);
            formData.append('filename', file.name);
        };

    });

