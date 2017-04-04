'use strict';

angular.module('socialAggregator')
    .controller('UploadController', function () {
        var vm = this;

        vm.dropzoneConfig = {
            parallelUploads: 10,
            maxFileSize: 10,
            url: 'api/files',
            headers: {
                Authorization: 'Token aaa'
            }
        };

    });

