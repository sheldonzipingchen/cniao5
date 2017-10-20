define(function(require, exports, module) {

    var Validator = require('bootstrap.validator');
    var Notify = require('common/bootstrap-notify');
    require('common/validator-rules').inject(Validator);





    exports.run = function() {



         if($("#teacher-add-form").length>0){




            require("jquery-chosen")
            require("jquery-chosen-css")


            var usersElm =$("#user-list");

            $.get(usersElm.data("get-url"),function(data){


                var users = JSON.parse(data);

                $.each(users ,function(i,n){

                    $("<option value='"+n.id+"'> "+n.username+"</option>").appendTo(usersElm);
                })

                 usersElm.chosen()

            });


            $("#rate").chosen();


            var $form = $("#teacher-add-form");
            var validator = new Validator({
            element: $form,
            failSilently: true,
             autoSubmit: false,
            onFormValidated: function(error){


                if (error) {
                    return false;
                }






                var model ={}
                model.teacher_name = $("#teacher_name").val();
                model.idcard = $("#id_num").val();
                model.rate = $("#rate").val();
                model.user_id = $("#user-list").val();
                model.company = $("#company").val();
                model.brief = $("#brief").val();
                model.logo_url = $form.data("logo-url")

                if(model.logo_url==undefined || model.logo_url==''){
                    Notify.warning("请先上传头像");
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

                            Notify.success("保存成功")

                        } else {
                            Notify.danger(data.message);
                        }
                    },
                    error: function(data) {
                        $('#btn-save').removeClass('disabled');
                        Notify.danger('系统错误！');
                    }
                });
            }
        });

            validator.addItem({
                element: '[name="teacher_name"]',
                required: true,
                display:'姓名'

             });
            validator.addItem({
                    element: '[name="id_num"]',
                    required: true,
                    display:'身份证',
                    rute:'idcard'

                 });
            validator.addItem({
                    element: '[name="rate"]',
                    required: true,
                    display:'分成'

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

        }





    };



});