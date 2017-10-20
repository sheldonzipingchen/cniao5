define(function(require, exports, module) {
    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);
    var Notify = require('common/bootstrap-notify');



    Validator.addRule(
        'sms_code_check',
        function(options, commit) {
            var element = options.element,
                    url = options.url ? options.url : (element.data('url') ? element.data('url') : null);
            value = element.val().replace(/\./g, "!");
            var phone = $('#register_mobile').val();
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


    exports.run = function() {

        var $form = $('#bind-exist-form');
        var validator = new Validator({
            element: $form,
            autoSubmit: false,
            onFormValidated: function(error, results, $form) {
                if (error) {
                    return false;
                }
                //$form.find('[type=submit]').button('loading');
                $("#bind-exist-form-error").hide();
                $.ajax({
                    url: $form.attr('action'),
                    data: $form.serialize(),  //JSON.stringify(strToObj($form.serialize())), //中文转码
                    //contentType: "application/json; charset=utf-8",   ///普通表单提交注释, contentType.
                     //dataType:'json',
                    type:"POST",
                    success: function(response) {
                        if (!response.success) {
                            Notify.danger(response.message);
                            $("#bind-exist-form-error").html(response.message).show();
                            return ;
                        }else{
                            Notify.success('绑定帐号成功，正在跳转至首页！');
                            window.setTimeout("location.href='/'",3000);
                        }
                    },
                    error: function(data) {
                        Notify.danger('系统错误！');
                    }
                });

            },
            failSilently: true

        });

        validator.addItem({
            element: '#bind-email-field',
            required: true,
            rule: 'email_or_mobile'
        });
        validator.addItem({
            element: '#bind-password-field',
            required: true
        });

        $("#a_new").click(function(){
            $("#a_new").addClass("active")
            $("#panel_new").addClass("active");
            $("#a_bind").removeClass("active")
            $("#panel_bind").removeClass("active");
        });

        $("#a_bind").click(function(){
            $("#a_bind").addClass("active")
            $("#panel_bind").addClass("active");
            $("#a_new").removeClass("active")
            $("#panel_new").removeClass("active");
        });


        var $newform = $('#set-bind-new-form');

        var validator_n = new Validator({
            element: $newform,
            autoSubmit: false,
            onFormValidated: function(error, results, $form) {
                if (error) {
                    return false;
                }
                if(!$('#user_terms').find('input[type=checkbox]').attr('checked')) {
                    Notify.danger('勾选同意此服务协议，才能继续注册！');
                    return ;
                }
                //$newform.find('[type=submit]').button('loading');
                $("#bind-new-form-error").hide();
                $.ajax({
                    url: $form.attr('post-url'),
                    data: $newform.serialize(),
                    /*contentType: "application/json; charset=utf-8",
                    dataType:'json',*/
                    type:"POST",
                    success: function(data) {
                        if (data.success) {
                            Notify.success('注册并绑定成功, 正在跳转至首页！');
                            window.setTimeout("location.href='/'", 3000);
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

        $('#user_terms input[type=checkbox]').on('click', function() {
            if($(this).attr('checked')) {
                $(this).attr('checked',false);
            } else {
                $(this).attr('checked',true);
            };
        });


        if ($('#register_mobile').length > 0) {
            $('.email_mobile_msg').removeClass('hidden');
            validator_n.addItem({
                element: '#register_mobile',
                required: true,
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
        }

        if($("#set_bind_username").length > 0){
            validator_n.addItem({
                element: '#set_bind_username',
                required: true,
                rule: 'chinese_alphanumeric byte_minlength{min:4} byte_maxlength{max:18} remote'
            });
        }

        validator_n.addItem({
            element: '#register_password',
            required: true,
            rule: 'minlength{min:5} maxlength{max:20}',
            display: '密码'
        });

        /*validator_n.addItem({
            element: '#user_terms',
            required: true,
            errormessageRequired: '勾选同意此服务协议，才能继续注册'
        });*/


        /**手机失焦事件*/
        $("#register_mobile").blur(function(){
            var mobile  = $("#register_mobile").val();
            emSmsCodeValidate(mobile);
        });

        function emSmsCodeValidate(mobile){

            var reg_mobile = /^1\d{10}$/;
            var isMobile = reg_mobile.test(mobile);
            if(isMobile){
                validator_n.addItem({
                    element: '#sms_code',
                    required: true,
                    rule: 'integer fixedLength{len:4} sms_code_check',//remote
                    display: '短信验证码'
                });
                $newform.on('click','.js-sms-send',function(e){
                    smsSend($('#register_mobile').val());
                    return;
                })

            }else{
                validator_n.removeItem('[name="sms_code"]');
            }
        }

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
            var url = '/auth/reg/send_message/'+mobi; //this.get("url");
            var data = {};
            data.to = mobi; //$('[name="'+this.get("dataTo")+'"]').val();
            $.get(url,data,function(response){
                if (("undefined" != typeof response['success'])&&(response['success']==true)) {
                    $('#js-time-left').html('120');
                    $('#js-fetch-btn-text').html('秒后重新获取');
                    Notify.success('发送短信成功');
                    $('.js-sms-send').addClass('disabled');
                    refreshTimeLeft();
                } else {
                    if ("undefined" != typeof response['error']){
                        Notify.danger(response['error']);
                    }else{
                        Notify.danger('发送短信失败，请联系管理员');
                    }
                }
            });
        }


    };


});