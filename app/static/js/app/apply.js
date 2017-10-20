define(function(require, exports, module) {

    var Validator = require('bootstrap.validator');
      var Notify = require('common/bootstrap-notify');
    require('common/validator-rules').inject(Validator);
    require('cniao-ckeditor');






    exports.run = function() {




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
                    profile.class_id = $form.data('class-id')
                    profile.real_name=$("#realname").val();
                    profile.qq=$("#qq").val();
                    profile.company=$("#company").val();
                    profile.mobi=$("#mobi").val();
                    profile.email=$("#email").val();
                    profile.work_year=$("#workyear").val();



                  $.ajax({
                    url:  $form.data('post-url'),
                    data: JSON.stringify(profile),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {


                        if (data.result) {
                            Notify.success('报名成功,我们将会在3个工作日内处理！');

                            setTimeout(function(){

                                window.location.href=$form.data('back-url');
                            },2000)

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
            element: '[name="realname"]',
            rule: 'chinese minlength{min:2} maxlength{max:12}',
            required: true,
        });


        validator.addItem({
            element: '[name="qq"]',
            rule: 'qq',
            required: true,

        });



        validator.addItem({
            element: '[name="mobi"]',
            rule: 'mobile',
            required: true,
        });


        validator.addItem({
            element: '[name="company"]',
            rule: 'chinese minlength{min:4} maxlength{max:50}',
            required: true,
        });
        validator.addItem({
                element: '[name="emaul"]',
                rule: 'email',
            required: true,
            });





    };



});