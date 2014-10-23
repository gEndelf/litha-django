(function () {
    angular
        .module('companiesApp', [
            'ui.router',
            'angularFileUpload'
        ])
        .config(stateConfig)
        .controller('CompanyListController', CompanyListController)
        .controller('CompanyFormController', CompanyFormController)
        .directive('serverError', serverError);

    function stateConfig($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/companies');
        $stateProvider
            .state('company_list', {
                url: '/companies',
                templateUrl: '/static/companies/partials/companies.html',
                controller: 'CompanyListController'
            })
            .state('company_form', {
                url: '/companies/:companyId',
                templateUrl: '/company_form/',
                controller: 'CompanyFormController'
            });
    }

    function CompanyListController($scope, $http) {
        $scope.companies = [];

        $scope.fetchCompanies = function () {
            $http.get('/companies/').success(function (data) {
                $scope.companies = data.companies;
            });
        };

        $scope.fetchCompanies();
    }

    function CompanyFormController($scope, $stateParams, $http, $location, FileUploader) {
        $scope.company = {};
        $scope.errors = {};
        $scope.uploader = new FileUploader({
            url: '/companies/' + $stateParams.companyId + '/',
            method: 'POST',
            alias: 'logo',
            autoUpload: true,
            onAfterAddingFile: function (item) {
                $scope.company_form.logo.$dirty = true;
                $scope.company_form.logo.$setValidity('server', true);
            },
            onCompleteItem: function (item, response) {
                if (response.error) {
                    $scope.company_form.logo.$setValidity('server', false);
                    $scope.errors.logo = response.error;
                } else {
                    $scope.company.logo = response.url;
                }
            }
        });

        $scope.fetchCompany = function (companyId) {
            $http.get('/companies/' + companyId + '/').success(function (data) {
                $scope.company = data.company;
            });
        };

        $scope.submitForm = function () {
            $http.put('/companies/' + $scope.company.id + '/', $scope.company).success(function (data) {
                if (data.errors) {
                    angular.forEach(data.errors, function (errors, field) {
                        $scope.company_form[field].$setValidity('server', false);
                        $scope.errors[field] = errors.join(', ');
                    });
                } else {
                    $location.path('/companies');
                }
            });
        };

        $scope.fetchCompany($stateParams.companyId);
    }

    function serverError() {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, element, attrs, ctrl) {
                ctrl.$parsers.unshift(function (value) {
                    ctrl.$setValidity('server', true);
                    return value;
                });
            }
        };
    }
})();
