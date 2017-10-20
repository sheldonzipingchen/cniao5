define(function(require, exports, module) {

    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);
//    var SmsSender = require('../widget/sms-sender');
    var Notify = require('common/bootstrap-notify');

    Validator.addRule(
        'email_or_mobile_check',
        function(options, commit) {
            var emailOrMobile = options.element.val();
            var reg_email = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            var reg_mobile = /^1\d{10}$/;
            var result =false;
            var isEmail = reg_email.test(emailOrMobile);
            var isMobile = reg_mobile.test(emailOrMobile);
            if (isEmail || isMobile) {
                result = true;
            }
            return  result;
        },
        "{{display}}格式错误"
    );



    exports.run = function() {

        var $form = $('#bind-user-form');

        ///表单验证
        var validator = new Validator({
            element: $form,
            autoSubmit: false,
            onFormValidated: function(error, results, $form) {
                if (error) {
                    return false;
                }

                var btnBind = $("#btn-bind");
                btnBind.button('submiting').addClass('disabled');

                var data={};
                data.mobi=$("#emailOrMobile").val();
                data.password=$("#password").val();

                $.ajax({
                    url:  $form.data('post-url'),
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {
                        if (data.success) {
                            Notify.success('恭喜你,绑定成功！');
                            window.setTimeout("location.href='/'",2000);
                        } else {
                            Notify.danger(data.message);
                            btnBind.button('reset').removeClass('disabled');
                        }
                    },
                    error: function(data) {
                        Notify.danger('系统错误！');
                        btnBind.button('reset').removeClass('disabled');
                    }
                });

            },
            failSilently: true
        });



        if ($('input[name="emailOrMobile"]').length > 0) {

            validator.addItem({
                element: '[name="emailOrMobile"]',
                required: true,
                rule: ' email_or_mobile_check',
                display:"手机号码/邮箱",
                onItemValidated: function(error, message, eleme) {

                }
            });
        }


        validator.addItem({
            element: '[name="password"]',
            required: true,
            rule: 'minlength{min:5} maxlength{max:20}',
            display: '密码'
        });



    };

});