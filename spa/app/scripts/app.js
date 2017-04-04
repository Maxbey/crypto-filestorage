'use strict';

angular
    .module('socialAggregator', [
        'ngAnimate',
        'ngAria',
        'ngCookies',
        'ngMessages',
        'ngResource',
        'ui.router',
        'ngSanitize',
        'ngMaterial',
        'satellizer',
        'ngDropzone',
        'validation.match'
    ])
    .config(function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider, $authProvider, $mdThemingProvider) {
        $urlRouterProvider.otherwise('/');
        $httpProvider.defaults.withCredentials = true;

        $mdThemingProvider.theme('default')
            .primaryPalette('indigo')
            .accentPalette('red');

        $stateProvider
            .state('enter', {
                abstract: true,
                data: {},
                views: {
                    header: {
                        templateUrl: 'views/header.html'
                    },
                    main: {}
                }
            })
            .state('enter.login', {
                url: '/login/',
                views: {
                    'main@': {
                        templateUrl: 'views/login.html'
                    }
                }
            })
            .state('enter.register', {
                url: '/register/',
                views: {
                    'main@': {
                        templateUrl: 'views/register.html'
                    }
                }
            });

        $stateProvider
            .state('app', {
                abstract: true,
                data: {
                    auth: true
                },
                views: {
                    header: {
                        templateUrl: 'views/header.logged.html'
                    },
                    main: {}
                }
            })
            .state('app.dashboard', {
                url: '/',
                views: {
                    'main@': {
                        templateUrl: 'views/dashboard.html'
                    }
                }
            })
            .state('app.upload', {
                url: '/upload/',
                views: {
                    'main@': {
                        templateUrl: 'views/upload.html'
                    }
                }
            })
            .state('app.manage-groups', {
                url: '/manage-groups/',
                views: {
                    'main@': {
                        templateUrl: 'views/manage.groups.html'
                    }
                }
            });

        $locationProvider.html5Mode({
            enabled: true,
            requiredBase: false
        });

        $authProvider.withCredentials = true;
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';

        $authProvider.loginUrl = 'http://api.cryptoapp.dev/api/auth/login/';

        $authProvider.authToken = 'Token';
        $authProvider.tokenType = 'Token';
        $authProvider.storageType = 'localStorage';
    }).run(function ($rootScope, $state, $auth, AuthenticationService) {
    var registrationCallback = $rootScope.$on("$stateChangeStart", AuthenticationService.stateControl);
    $rootScope.$on('$destroy', registrationCallback);
});
