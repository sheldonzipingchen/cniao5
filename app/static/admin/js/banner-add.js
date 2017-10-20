
define(function(require, exports, module) {



    require("layer")
    require("layer-css")
    require("plupload")
    require("qiniu")
    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);




     var $form = $("#add-form");
     var validator = new Validator({
            element: $form,
            failSilently: true,
             autoSubmit: false,
            onFormValidated: function(error){


                if (error) {
                    return false;
                }



                var model ={}
                model.redirect_url = $("#redirect_url").val();
                model.bg_color = $("#bg_color").val();
                model.order_num = $("#order_num").val();
                model.img_url = $form.data("logo-url")
                model.is_blank=$('input:radio[name=is_blank]:checked').val();



                if(model.img_url==undefined || model.img_url==''){

                    layer.msg("请先上传图片")
                    return false
                }


                $('#btn-save').addClass('disabled');

                  $.ajax({
                    url:  $form.data('post-url'),
                    data: JSON.stringify(model),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                        $('#btn-save').removeClass('disabled');
                        if (data.success) {

                            $form[0].reset()

                            layer.msg("保存成功");
                            window.location.href='/admin/banners.html'

                        } else {
                             layer.msg(data.message);
                        }
                    },
                    error: function(data) {
                        $('#btn-save').removeClass('disabled');
                         layer.msg('系统错误！');
                    }
                });
            }
        });

            validator.addItem({
                element: '[name="redirect_url"]',
                required: true,
                display:'目标地址',
                rule: 'url'

             });
            validator.addItem({
                    element: '[name="bg_color"]',
                    required: true,
                    display:'颜色值',

                 });
            validator.addItem({
                    element: '[name="is_blank"]',
                    required: true,
                    display:'打开模式'

                 });
        validator.addItem({
                        element: '[name="order_num"]',
                        required: true,
                        display:'排序'

                     });




    var tokenUrl =  $("#img-block").data("token-url")

    var uploader = Qiniu.uploader({
                            runtimes: 'html5,flash,html4',    //上传模式,依次退化
                            browse_button: 'pickfiles',       //上传选择的点选按钮，**必需**
                            uptoken_url: tokenUrl,            //Ajax请求upToken的Url，**强烈建议设置**（服务端提供）
                             unique_names: true, // 默认 false，key为文件名。若开启该选项，SDK为自动生成上传成功后的key（文件名）。
                            // save_key: true,   // 默认 false。若在服务端生成uptoken的上传策略中指定了 `sava_key`，则开启，SDK会忽略对key的处理
                            domain: 'http://cniao5-imgs.qiniudn.com/',   //bucket 域名，下载资源时用到，**必需**
                            get_new_uptoken: false,  //设置上传文件的时候是否每次都重新获取新的token
                            container: 'img-block',           //上传区域DOM ID，默认是browser_button的父元素，
                            max_file_size: '2mb',           //最大文件体积限制
                            flash_swf_url: '/static/libs/plupload/Moxie.swf',  //引入flash,相对路径
                            max_retries: 3,                   //上传失败最大重试次数
                            dragdrop: true,                   //开启可拖曳上传
                            drop_element: 'container',        //拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
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


                                    $(".screenshot-container" ).find('.progress').show()

                                },
                                'BeforeUpload': function(up, file) {
                                       // 每个文件上传前,处理相关的事情
                                },
                                'UploadProgress': function(up, file) {

                                    var percent = file.percent;
                                    $(".screenshot-container" ).find('.progress-bar').css({"width": percent + "%"});

                                },
                                'FileUploaded': function(up, file, info) {

                                     console.log("info="+info)

                                    var res = JSON.parse(info)
                                    var domain = up.getOption('domain');
                                    var sourceLink = domain + res.key; //获取上传成功后的文件的Url

                                    $("#img_url").attr({"src":sourceLink});
                                    $("#img_url").show();
                                    $form.attr('data-logo-url',sourceLink)

                                    $(".screenshot-container" ).find('.progress').css({"display":"none"})

                                },
                                'Error': function(up, err, errTip) {
                                       //上传出错时,处理相关的事情
                                },
                                'UploadComplete': function() {
                                       //队列文件处理完毕后,处理相关的事情
                                }

                            }
                        });

});


