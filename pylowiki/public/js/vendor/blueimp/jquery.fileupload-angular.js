/*
 * jQuery File Upload AngularJS Plugin 1.0.1
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2013, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint nomen: true, unparam: true */
/*global angular */

(function () {
    'use strict';

	    angular.module('blueimp.fileupload', [])
	
	        .provider('fileUpload', function () {
	            var scopeApply = function () {
	                    var scope = angular.element(this)
	                        .fileupload('option', 'scope')();
	                    if (!scope.$$phase) {
	                        scope.$apply();
	                    }
	                },
	                $config;
	            $config = this.defaults = {
	                handleResponse: function (e, data) {
	                    var files = data.result && data.result.files;
	                    if (files) {
	                        data.scope().replace(data.files, files);
	                    } else if (data.errorThrown ||
	                            data.textStatus === 'error') {
	                        data.files[0].error = data.errorThrown ||
	                            data.textStatus;
	                    }
	                },
	                add: function (e, data) {
	                    var scope = data.scope();
						console.log("add data: ");
	                    console.log(data);
	                    console.log("Param info: ");
	                    var fileType = data.paramName[0];
	                    scope.fuType = fileType;
	                    console.log(fileType);
	                    data.process(function () {
	                        return scope.process(data);
	                    }).always(
	                        function () {                            
	                            var file = data.files[0],
	                                submit = function () {
	                                	console.log("submit data: ");
	                                    console.log(data);
	                                    return data.submit();
	                                };
	                            file.$cancel = function () {
	                                scope.clear(data.files);
                                return data.abort();
                            };
                            file.$state = function () {
                                return data.state();
                            };
                            file.$progress = function () {
                                return data.progress();
                            };
                            file.$response = function () {
                                return data.response();
                            };
                            if (file.$state() === 'rejected') {
                                file._$submit = submit;
                            } else {
                                file.$submit = submit;
                            }
                            scope.$apply(function () {
                            	console.log("Apply is always called?");
                                var method = scope.option('prependFiles') ?
                                        'unshift' : 'push';
                                Array.prototype[method].apply(
                                    scope.queue,
                                    data.files
                                );
                                if (file.$submit &&
                                        (scope.option('autoUpload') ||
                                        data.autoUpload) &&
                                        data.autoUpload !== false) {
                                    file.$submit();
                                }
                            });
                        }
                    );
                },
                progress: function (e, data) {
                    data.scope().$apply();
                },
                done: function (e, data) {
                    var that = this;
                    data.scope().$apply(function () {
                        data.handleResponse.call(that, e, data);
                    });
                },
                fail: function (e, data) {
                    var that = this;
                    if (data.errorThrown === 'abort') {
                        return;
                    }
                    if (data.dataType.indexOf('json') === data.dataType.length - 4) {
                        try {
                            data.result = angular.fromJson(data.jqXHR.responseText);
                        } catch (err) {}
                    }
                    data.scope().$apply(function () {
                        data.handleResponse.call(that, e, data);
                    });
                },
                stop: scopeApply,
                processstart: scopeApply,
                processstop: scopeApply,
                getNumberOfFiles: function () {
                    return this.scope().queue.length;
                },
                dataType: 'json',
                prependFiles: true,
                autoUpload: false
            };
            
            this.$get = [
                function () {
                    return {
                        defaults: $config
                    };
                }
            ];
        })

        .provider('formatFileSizeFilter', function () {
            var $config = this.defaults = {
                // Byte units following the IEC format
                // http://en.wikipedia.org/wiki/Kilobyte
                units: [
                    {size: 1000000000, suffix: ' GB'},
                    {size: 1000000, suffix: ' MB'},
                    {size: 1000, suffix: ' KB'}
                ]
            };
            this.$get = function () {
                return function (bytes) {
                    if (!angular.isNumber(bytes)) {
                        return '';
                    }
                    var unit = true,
                        i = -1;
                    while (unit) {
                        unit = $config.units[i += 1];
                        if (i === $config.units.length - 1 || bytes >= unit.size) {
                            return (bytes / unit.size).toFixed(2) + unit.suffix;
                        }
                    }
                };
            };
        })

        .controller('FileUploadController', [
            '$scope', '$element', '$attrs', 'fileUpload', '$http',
            function ($scope, $element, $attrs, fileUpload, $http) {
            console.log("1");
            console.log($scope);
            console.log($scope.fuType);
                $scope.disabled = angular.element('<input type="file">')
                    .prop('disabled');
                $scope.uploadImage = false;
                $scope.submitStatus = '-1';
                $scope.queue = $scope.queue || [];
                $scope.setImageSource = function () {
                    var data = {'source': $scope.imageSource};
                    $http.post("/profile/" + $scope.code + "/" + $scope.url + "/picture/set/image/source", data)
                        .success(function(result){
                            if (result.statusCode === 1){
                                $scope.submitStatus = 1;
                            }
                            else{
                                $scope.submitStatus = 0;
                            }
                        }
                    );
                };
                $scope.clear = function (files) {
                    var queue = this.queue,
                        i = queue.length,
                        file = files,
                        length = 1;
                    if (angular.isArray(files)) {
                        file = files[0];
                        length = files.length;
                    }
                    while (i) {
                        if (queue[i -= 1] === file) {
                            return queue.splice(i, length);
                        }
                    }
                };
                $scope.replace = function (oldFiles, newFiles) {
                    var queue = this.queue,
                        file = oldFiles[0],
                        i,
                        j;
                    for (i = 0; i < queue.length; i += 1) {
                        if (queue[i] === file) {
                            for (j = 0; j < newFiles.length; j += 1) {
                                queue[i + j] = newFiles[j];
                            }
                            return;
                        }
                    }
                };
                $scope.progress = function () {
                    return $element.fileupload('progress');
                };
                $scope.active = function () {
                    return $element.fileupload('active');
                };
                $scope.option = function (option, data) {
                    return $element.fileupload('option', option, data);
                };
                $scope.add = function (data) {
                    return $element.fileupload('add', data);
                };
                $scope.send = function (data) {
                    return $element.fileupload('send', data);
                };
                $scope.process = function (data) {
                	console.log("Data in process:");
                	console.log(data);
                    return $element.fileupload('process', data);
                };
                $scope.processing = function (data) {
                    return $element.fileupload('processing', data);
                };
                $scope.applyOnQueue = function (method) {
                    var list = this.queue.slice(0),
                        i,
                        file;
                    for (i = 0; i < list.length; i += 1) {
                        file = list[i];
                        if (file[method]) {
                            file[method]();
                        }
                    }
                };
                $scope.submit = function () {
                    this.applyOnQueue('$submit');
                };
                $scope.cancel = function () {
                    this.applyOnQueue('$cancel');
                };
                // The fileupload widget will initialize with
                // the options provided via "data-"-parameters,
                // as well as those given via options object:
                $element.fileupload(angular.extend(
                    {scope: function () {
                        return $scope;
                    }},
                    fileUpload.defaults
                )).on('fileuploadadd', function (e, data) {
                    data.scope = $scope.option('scope');
                }).on([
                    'fileuploadadd',
                    'fileuploadsubmit',
                    'fileuploadsend',
                    'fileuploaddone',
                    'fileuploadfail',
                    'fileuploadalways',
                    'fileuploadprogress',
                    'fileuploadprogressall',
                    'fileuploadstart',
                    'fileuploadstop',
                    'fileuploadchange',
                    'fileuploadpaste',
                    'fileuploaddrop',
                    'fileuploaddragover',
                    'fileuploadchunksend',
                    'fileuploadchunkdone',
                    'fileuploadchunkfail',
                    'fileuploadchunkalways',
                    'fileuploadprocessstart',
                    'fileuploadprocess',
                    'fileuploadprocessdone',
                    'fileuploadprocessfail',
                    'fileuploadprocessalways',
                    'fileuploadprocessstop'
                ].join(' '), function (e, data) {
                    $scope.$emit(e.type, data);
                });
                // Observe option changes:
                $scope.$watch(
                    $attrs.fileupload,
                    function (newOptions, oldOptions) {
                        if (newOptions) {
                            $element.fileupload('option', newOptions);
                        }
                    }
                );
            }
        ])

        .controller('FileUploadProgressController', [
            '$scope', '$attrs', '$parse',
            function ($scope, $attrs, $parse) {
            	console.log("2");
            	console.log($scope);
                var fn = $parse($attrs.progress),
                    update = function () {
                        var progress = fn($scope);
                        if (!progress || !progress.total) {
                            return;
                        }
                        $scope.num = Math.floor(
                            progress.loaded / progress.total * 100
                        );
                    };
                update();
                $scope.$watch(
                    $attrs.progress + '.loaded',
                    function (newValue, oldValue) {
                        if (newValue !== oldValue) {
                            update();
                        }
                    }
                );
            }
        ])
        

        .controller('FileUploadPreviewController', [
            '$scope', '$element', '$attrs', '$parse',
            function ($scope, $element, $attrs, $parse) {
	            console.log("3");
	            console.log($attrs);
	            console.log($scope.fuType);
                var fn = $parse($attrs.preview),
                    file = fn($scope);
                    console.log(file);
                if (file.preview) {
                    $element.append(file.preview);
                    var height = $element[0].clientHeight; // what the user sees
                    var width = $element[0].clientWidth; // what the user sees
                    var selectedWidth = 100; // The default selection width
                    var selectedHeight = 100; // The default selection height
                    var startX = (width/2) - (selectedWidth/2);
                    var startY = (height/2) - (selectedHeight/2);
                    //var maxDims = [$("#setImageSourceForm").width(), $("#setImageSourceForm").width()];
                    if ($scope.fuType === "files[]"){
	                    $element.Jcrop({
	                        //bgColor:     'black',
	                        bgOpacity:   0.4,
	                        aspectRatio: 1,
	                        boxWidth:   400,
	                        //boxHeight:  $("#setImageSourceForm").width(),
	                        setSelect:   [ startX, startY, startX + selectedWidth, startY + selectedHeight ], //array [ x, y, x2, y2 ]
	                        // this setSelect is actually a bit off due to the $element getting resized once the image is in place.
	                        onChange: function(c){
	                            /*
	                            * c.w   ->  width
	                            * c.h   ->  length
	                            * c.x   ->  x coordinate of upper-left corner
	                            * c.x2  ->  y coordinate of upper-left corner
	                            * c.y   ->  x coordinate of lower-right corner
	                            * c.y2  ->  y coordinate of lower-right corner
	                            */
	                            file.width = c.w;
	                            file.x = c.x;
	                            file.y = c.y;
	                        }
	                    });
                    };
                }
            }
        ])
        
        .directive('fileupload', function () {
            return {
                controller: 'FileUploadController'
            };
        })

        .directive('progress', function () {
            return {
                controller: 'FileUploadProgressController'
            };
        })

        .directive('preview', function () {
            return {
                controller: 'FileUploadPreviewController'
            };
        })
        
        /*
.directive('fileType', function () {
	        return {
		      scope: {
			      fileType: '=f'
		      };  
	        };
        })
*/
        
        .directive('download', function () {
            return function (scope, elm, attrs) {
                elm.on('dragstart', function (e) {
                    try {
                        e.originalEvent.dataTransfer.setData(
                            'DownloadURL',
                            [
                                'application/octet-stream',
                                elm.prop('download'),
                                elm.prop('href')
                            ].join(':')
                        );
                    } catch (err) {}
                });
            };
        });

}());				
