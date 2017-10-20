define(function(require, exports, module) {

    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);

    require("layer")
    require("layer-css")



    exports.run = function() {





        var $form = $("#login-form")
        var validator = new Validator({
            element: $form,
            failSilently: true,
             autoSubmit: false,
            onFormValidated: function(error){


                if (error) {
                    return false;
                }


                $('.login-btn').addClass('disabled');


                    var accountModel={};

                    accountModel.account=$("#account").val()
                    accountModel.password=$("#pwd").val()



                  $.ajax({
                    url:  $form.data('post-url'),
                    data: JSON.stringify(accountModel),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {


                        if (data.success) {

                           window.location.href=$form.data('go-url');

                        } else {
                            layer.msg(data.message);
                        }
                    },
                    error: function(data) {
                        layer.msg("系统错误");
                    }
                });
            }
        });

        validator.addItem({
            element: '[name="login_account"]',
            required: true,

        });


        validator.addItem({
            element: '[name="login_pwd"]',
            required: true

        });




    };



});