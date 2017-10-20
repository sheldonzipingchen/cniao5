define(function(require, exports, module) {

    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);
//    var SmsSender = require('../widget/sms-sender');
    var Notify = require('common/bootstrap-notify');

    Validator.addRule(
        'email_or_mobile_check',
        function(options, commit) {
            var emailOrMobile = options.element.val();
            //var reg_email = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            var reg_mobile = /^1\d{10}$/;
            var result =false;
            //var isEmail = reg_email.test(emailOrMobile);
            var isMobile = reg_mobile.test(emailOrMobile);
            if(isMobile){
                //$(".email_mobile_msg").removeClass('hidden');
                //$('.js-captcha').addClass('hidden');
                $('.js-sms-send').removeClass('disabled');
            }else {
                //$(".email_mobile_msg").addClass('hidden');
                //$('.js-sms-send').addClass('disabled');
                $('.js-captcha').removeClass('hidden');
            }
            if (isEmail || isMobile) {
                result = true;
            }
            return  result;
        },
        "{{display}}格式错误"
    );

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
        var $form = $('#register-form');

        ///表单验证
        var validator = new Validator({
            element: $form,
            autoSubmit: false,
            onFormValidated: function(error, results, $form) {
                if (error) {
                    return false;
                }
                $('#register-btn').button('submiting').addClass('disabled');

                var data={};
                data.mobi=$("#register_mobile").val();
                data.password=$("#register_password").val();
                data.username=$("#register_username").val();
                data.regtype=$form.data("reg-type");

                $.ajax({
                    url:  $form.data('post-url'),
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",   ///普通表单提交注释, contentType
                    dataType:'json',
                    type:"POST",
                    success: function(data) {
                        if (data.success) {
                            Notify.success('恭喜你,注册成功！');
                            window.setTimeout("location.href='/'",2000);
                        } else {
                            Notify.danger(data.message);
                            $('#register-btn').button('reset').removeClass('disabled');
                        }
                    },
                    error: function(data) {
                        Notify.danger('系统错误！');
                        $('#register-btn').button('reset').removeClass('disabled');
                    }
                });

            },
            failSilently: true
        });



        if ($('input[name="mobi"]').length > 0) {

            $('.email_mobile_msg').removeClass('hidden');
            validator.addItem({
                element: '[name="mobi"]',
                required: true,
                rule: 'phone email_or_mobile_remote',
                display:"手机号码",
                onItemValidated: function(error, message, eleme) {
                    console.log(error);
                    if (error) {
                        $('.js-sms-send').addClass('disabled');
                        return;
                    } else {
                        $('.js-sms-send').removeClass('disabled');

                    }
                }
            });
        }

         if ($('input[name="username"]').length > 0) {


             validator.addItem({
                element: '[name="username"]',
                required: true,
                 display:"用户名",
                rule: 'chinese_alphanumeric byte_minlength{min:4} byte_maxlength{max:18} remote'
            });

         }



        validator.addItem({
            element: '[name="password"]',
            required: true,
            rule: 'minlength{min:5} maxlength{max:20}',
            display: '密码'
        });

        validator.addItem({
                    element: '[name="sms_code"]',
                    required: true,
                    rule: 'integer fixedLength{len:4} sms_code_check',//remote
                    display: '短信验证码'
                });

        validator.addItem({
            element: '#user_terms',
            required: true,
            errormessageRequired: '勾选同意此服务协议，才能继续注册'
        });



          $form.on('click','.js-sms-send',function(e){
                    smsSend($('#register_mobile').val());
                    return;
           })



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

        function strToObj(str){
            str = str.replace(/&/g,"','");
            str = str.replace(/=/g,"':'");
            str = "({'"+str +"'})";
            obj = eval(str);
            return obj;
        }

    };

});