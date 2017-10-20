define(function(require, exports, module) {

    var Validator = require('bootstrap.validator');
      var Notify = require('common/bootstrap-notify');
    require('common/validator-rules').inject(Validator);

    exports.run = function() {



        var $form = $("#user-pwd-form")
        var validator = new Validator({
            element: $form,
            failSilently: true,
             autoSubmit: false,
            onFormValidated: function(error){
                if (error) {
                    return false;
                }


                $('#pwd-save-btn').button('submiting').addClass('disabled');

                var pwds={};
                pwds.new_pwd = $("#new_pwd").val();
                pwds.old_pwd = $("#old_pwd").val();

                $.ajax({
                    url:  $form.data('post-url'),
                    data: JSON.stringify(pwds),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                        $('#pwd-save-btn').button('reset').removeClass('disabled');

                        if (data.success) {
                            Notify.success('修改成功！');

                        } else {
                            Notify.danger(data.message);
                        }
                    },
                    error: function(data) {
                        Notify.danger('系统错误！');
                    }
                });
            }
        });




        validator.addItem({
            element: '#old_pwd',
            rule: 'password'
        });


        validator.addItem({
            element: '#new_pwd',
            rule: 'password'
        });

        validator.addItem({
            element: '#new_pwd_cfr',
            rule: "confirmation{target: '#new_pwd'}"
        });








    };

});