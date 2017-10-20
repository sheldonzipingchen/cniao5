define(function(require, exports, module) {

    var Validator = require('bootstrap.validator');
    var Notify = require('common/bootstrap-notify');
    require('common/validator-rules').inject(Validator);
    require("jquery-chosen")
    require("jquery-chosen-css")
    require("layer")
    require("layer-css")




   Validator.addRule(
        'sms_code_check',
        function(options, commit) {
            var element = options.element,
                    url = options.url ? options.url : (element.data('url') ? element.data('url') : null);
            value = element.val().replace(/\./g, "!");
            var phone = $('#mobi').val();
            var code =  $('#sms_code').val();
            if(phone == null || phone == ''){
                return false;
            }
            if(code == null || code == ''){
                return false;
            }
            var data = {};
            data.phone =phone;
            data.code = value
            data.use_for = 'reg';
            $.post(url, data, function(response){
                commit(response.success, response.message);
            }, 'json');
        },
        "{{display}}格式错误"
    );



   Validator.addRule(
        'email_code_check',
        function(options, commit) {
            var element = options.element,
                    url = options.url ? options.url : (element.data('url') ? element.data('url') : null);
            value = element.val().replace(/\./g, "!");
            var email = $('#email').val();
            var code =  $('#email_code').val();
            if(email == null || email == ''){
                return false;
            }
            if(code == null || code == ''){
                return false;
            }
            var data = {};
            data.email =email;
            data.code = value
            $.post(url, data, function(response){
                commit(response.success, response.message);
            }, 'json');
        },
        "{{display}}格式错误"
    );



    exports.run = function() {



        $("#txt_edit_username").on("click",function(){


            layer.open({

                type:1,
                title:'修改用户名',
                area:["600px"],
                offset: ['100px'],
                content:$("#dialog-modify-username")


             });





        });

         var formModifyUsername = $('#form-modify-username');

        ///表单验证
        var validator_username = new Validator({
            element: formModifyUsername,
            autoSubmit: false,
            onFormValidated: function(error, results, $form) {
                if (error) {
                    return false;
                }
                $('#modify-btn').button('submiting').addClass('disabled');

                var model={};

                model.val=$("#username").val();
                model.action='username';



                $.ajax({
                    url:  formModifyUsername.data('post-url'),
                    data: JSON.stringify(model),
                    contentType: "application/json; charset=utf-8",   ///普通表单提交注释, contentType
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                        $('#modify-btn').button('reset').removeClass("disabled")
                        if(data.success){
                            layer.closeAll();
                            $("#user_name").html(model.val);
                        }
                        else {
                             layer.msg(data.message);
                        }
                    },
                    error: function(data) {
                        $('#modify-btn').button('reset').removeClass("disabled")
                        layer.msg("系统错误,稍后重试");
                    }
                });

            },
            failSilently: true
        });


          validator_username.addItem({
                element: '[name="username"]',
                required: true,
                 display:"用户名",
                rule: 'chinese_alphanumeric byte_minlength{min:4} byte_maxlength{max:18} remote'
            });






        $("#profile_workyear").chosen();

        var $form = $("#user-profile-form")
        var validator = new Validator({
            element: $form,
            failSilently: true,
             autoSubmit: false,
            onFormValidated: function(error){
                if (error) {
                    return false;
                }
                $('#profile-save-btn').button('submiting').addClass('disabled');


                    var profile={};
                    profile.real_name=$("#profile_realname").val();
                    profile.addr=$("#profile_addr").val();
                    profile.qq=$("#profile_qq").val();
                    profile.company=$("#profile_company").val();
                    profile.job=$("#profile_job").val();
                    profile.work_year=$("#profile_workyear").val();
                    profile.about_me=$("#profile_about").val();


                  $.ajax({
                    url:  $form.data('post-url'),
                    data: JSON.stringify(profile),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                        $('#profile-save-btn').button('reset').removeClass('disabled');

                        if (data.success) {
                            Notify.success('修改成功！');

                        } else {
                            Notify.danger('修改失败！');
                        }
                    },
                    error: function(data) {
                        Notify.danger('系统错误！');
                    }
                });
            }
        });

        validator.addItem({
            element: '[name="profile[realname]"]',
            rule: 'chinese minlength{min:2} maxlength{max:12}'
        });

        validator.addItem({
            element: '[name="profile[addr]"]',
            rule: 'minlength{min:6} maxlength{max:50}'
        });



        validator.addItem({
            element: '[name="profile[qq]"]',
            rule: 'qq'
        });



        validator.addItem({
            element: '[name="profile[mobile]"]',
            rule: 'mobile'
        });


        validator.addItem({
            element: '[name="profile[company]"]',
            rule: ' minlength{min:2} maxlength{max:50}'
        });
        validator.addItem({
                element: '[name="profile[job]"]',
                rule: ' minlength{min:2} maxlength{max:50}'
            });






        if ($(".js-mobil-bind").length>0){

            $(".js-mobil-bind").on('click',function(){

                $("#mobi-dialog").modal('show');

            })



            var $form = $('#form-bind-mobile');

             $form.on('click','.js-sms-send',function(e){
                    smsSend($('#mobi').val());
                    return;
            })

            ///表单验证
            var validator_bind_mobile = new Validator({
                element: $form,
                autoSubmit: false,
                onFormValidated: function(error, results, $form) {
                    if (error) {
                        return false;
                    }

                    $('#bind-btn').button('submiting').addClass('disabled');
                    $.ajax({
                        url:  $form.data('post-url'),
                        data: $form.serialize(),
                        type:"POST",
                        success: function(data) {
                            console.log(data.success);
                            if (data.success) {
                                Notify.success('绑定成功！');
                                window.setTimeout("location.reload()",3000);
                            } else {
                                Notify.danger(data.message);
                            }
                        },
                        error: function(data) {
                            Notify.danger('系统错误！');
                        }
                    });

                },
                failSilently: true
            });




              validator_bind_mobile.addItem({
                element: '[name="mobi"]',
                required: true,
                display:'手机号',
                rule: 'phone remote',
                onItemValidated: function(error, message, eleme) {
                    if (error) {
                        $('.js-sms-send').addClass('disabled');
                        return;
                    } else {
                        $('.js-sms-send').removeClass('disabled');

                    }
                }
            });


               validator_bind_mobile.addItem({
                    element: '[name="sms_code"]',
                    required: true,
                    rule: 'integer fixedLength{len:4} sms_code_check',//remote
                    display: '短信验证码'
                });




        }


        if ($(".js-email-bind").length >0){


             $(".js-email-bind").on('click',function(){

                $("#email-dialog").modal('show');

            })


            var $form = $('#form-bind-email');

            $form.on('click','.js-email-send',function(e){
                    smsEmail($('#email').val());
                    return;
            })

            var validator_bind_email = new Validator({
                element: $form,
                autoSubmit: false,
                onFormValidated: function(error, results, $form) {
                    if (error) {
                        return false;
                    }

                    $('#bind-btn').button('submiting').addClass('disabled');
                    $.ajax({
                        url:  $form.data('post-url'),
                        data: $form.serialize(),
                        type:"POST",
                        success: function(data) {
                            console.log(data.success);
                            if (data.success) {
                                Notify.success('绑定成功！');
                                window.setTimeout("location.reload()",3000);
                            } else {
                                Notify.danger(data.message);
                            }
                        },
                        error: function(data) {
                            Notify.danger('系统错误！');
                        }
                    });


                },
                failSilently: true
            });


             validator_bind_email.addItem({
                element: '[name="email"]',
                required: true,
                display:'邮箱',
                rule: 'email remote',
                onItemValidated: function(error, message, eleme) {
                    if (error) {
                        $('.js-email-send').addClass('disabled');
                        return;
                    } else {
                        $('.js-email-send').removeClass('disabled');

                    }
                }
            });


              validator_bind_email.addItem({
                    element: '[name="email_code"]',
                    required: true,
                    rule: 'integer fixedLength{len:4} email_code_check',//remote
                    display: '验证码'
                });


        }



    };


     /**发送验证码*/
        function smsSend(mobi){
            var refreshTimeLeft = function(){
                var leftTime = $('#js-time-left').html();
                $('#js-time-left').html(leftTime-1);
                if (leftTime-1 > 0) {
                    setTimeout(refreshTimeLeft, 1000);
                } else {
                    $('#js-time-left').html('');
                    $('#js-fetch-btn-text').html('获取验证码');
                    $('.js-sms-send').removeClass('disabled');
                }
            };

            var leftTime = $('#js-time-left').html();
            if (leftTime.length > 0){
                return false;
            }
            var url = $(".js-sms-send").data("sms-url")


            var phone= mobi;
            $('.js-sms-send').addClass('disabled');
            $.get(url,'phone='+mobi,function(response){
                if (("undefined" != typeof response['success'])&&(response['success']==true)) {
                    $('#js-time-left').html('120');
                    $('#js-fetch-btn-text').html('秒后重新获取');
                    Notify.success('发送短信成功');
                    refreshTimeLeft();
                } else {
                    Notify.danger(response.message);
                }
            });
        }



         /**发送验证码*/
        function smsEmail(email){
            var refreshTimeLeft = function(){
                var leftTime = $('#js-time-left-email').html();
                $('#js-time-left-email').html(leftTime-1);
                if (leftTime-1 > 0) {
                    setTimeout(refreshTimeLeft, 1000);
                } else {
                    $('#js-time-left-email').html('');
                    $('#js-fetch-btn-text-email').html('获取验证码');
                    $('.js-email-send').removeClass('disabled');
                }
            };

            var leftTime = $('#js-time-left-email').html();
            if (leftTime.length > 0){
                return false;
            }
            var url = $(".js-email-send").data("url")


            $('.js-email-send').addClass('disabled');
            $.get(url,'email='+email,function(response){
                if (("undefined" != typeof response['success'])&&(response['success']==true)) {
                    $('#js-time-left-email').html('120');
                    $('#js-fetch-btn-text-email').html('秒后重新获取');
                    Notify.success('发送验证码成功');
                    refreshTimeLeft();
                } else {
                    Notify.danger(response.message);
                }
            });
        }

});