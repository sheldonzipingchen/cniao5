define(function(require, exports, module) {

    var Validator = require('bootstrap.validator');
    var Notify = require('common/bootstrap-notify');
    require('common/validator-rules').inject(Validator);





    exports.run = function() {





        var tokenUrl = $("body").data("token-url")


        var uploader = Qiniu.uploader({
                            runtimes: 'html5,flash,html4',    //上传模式,依次退化
                            browse_button: 'pickfiles',       //上传选择的点选按钮，**必需**
                            uptoken_url: tokenUrl,            //Ajax请求upToken的Url，**强烈建议设置**（服务端提供）
                             unique_names: true, // 默认 false，key为文件名。若开启该选项，SDK为自动生成上传成功后的key（文件名）。
                            // save_key: true,   // 默认 false。若在服务端生成uptoken的上传策略中指定了 `sava_key`，则开启，SDK会忽略对key的处理
                            domain: 'http://cniao5-imgs.qiniudn.com/',   //bucket 域名，下载资源时用到，**必需**
                            get_new_uptoken: false,  //设置上传文件的时候是否每次都重新获取新的token
                            container: 'screenshot-container',           //上传区域DOM ID，默认是browser_button的父元素，
                            max_file_size: '1mb',           //最大文件体积限制
                            flash_swf_url: '/static/libs/plupload/Moxie.swf',  //引入flash,相对路径
                            max_retries: 3,                   //上传失败最大重试次数
                            dragdrop: true,                   //开启可拖曳上传
                            drop_element: 'screenshot-container',        //拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
                            chunk_size: '4mb',                //分块上传时，每片的体积
                            auto_start: true,                 //选择文件后自动上传，若关闭需要自己绑定事件触发上传
                            filters: {
                                max_file_size: '1mb',
                                mime_types: [
                                    { title: "Image files", extensions: "jpg,gif,png,jpeg" }
                                ]
                            },
                            init: {
                                'FilesAdded': function(up, files) {

                                    $("body").find('.progress-bar').css({"width": 0 + "%"});

                                },
                                'BeforeUpload': function(up, file) {
                                       // 每个文件上传前,处理相关的事情
                                },
                                'UploadProgress': function(up, file) {

                                     var percent = file.percent;
                                    $("body").find('.progress-bar').css({"width": percent + "%"});

                                },
                                'FileUploaded': function(up, file, info) {


                                    var res = JSON.parse(info)
                                    var domain = up.getOption('domain');
                                    var sourceLink = domain + res.key; //获取上传成功后的文件的Url


                                    $(".img-list").append('<div class="col-md-3"><a href="#" class="thumbnail"><img src="'+sourceLink+'" ></a></div>')


                                     saveImge(sourceLink)

                                },
                                'Error': function(up, err, errTip) {
                                       //上传出错时,处理相关的事情
                                },
                                'UploadComplete': function() {
                                       //队列文件处理完毕后,处理相关的事情
                                }

                            }
                        });





        function  saveImge(img_url){



            var course_id = $("body").data("course-id");
            var model ={}
            model.course_id = course_id;
            model.img_url = img_url;



                    $.ajax({
                        'url': $("body").data('post-url'),
                        'type':'post',
                        'data':JSON.stringify(model),
                         contentType: "application/json; charset=utf-8",
                         success: function(data) {


                        },
                        'error': function(data) {
                            Notify.danger('保存失败');
                        }
                    });


        }



    };



});