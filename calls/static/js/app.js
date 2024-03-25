        angular.module('myApp', [])
            .controller('changeListController', function($scope, $http) {

                console.log("my controller")
                $scope.firstDropdownChanged = function() {
                    var selectedValue = $scope.firstDropdown;

                    // Make an AJAX request to fetch options for the second dropdown
                    $http.get('/get-dependent-options/', { params: { selected_value: selectedValue } })
                        .then(function(response) {
                            $scope.secondDropdownOptions = response.data.options;
                        }, function(error) {
                            // Handle error, if any
                        });
                };
            });