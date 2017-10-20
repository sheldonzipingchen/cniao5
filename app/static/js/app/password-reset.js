define(function(require, exports, module) {

    var Validator = require('bootstrap.validator');
//    var SmsSender = require('../widget/sms-sender');
    require('common/validator-rules').inject(Validator);
    var Notify = require('common/bootstrap-notify');


    exports.run = function() {


        if($("#password-reset-form").length >0){

               validator = new Validator({
                element: '#password-reset-form',
                onFormValidated: function(err, results, form) {
                    if (err == false) {
                        $('#password-reset-form').find("[type=submit]").button('loading');
                    }else{
                        $('#alertxx').hide();
                    };

                }

            });

            validator.addItem({
                element: '[name="email_phone"]',
                required: true,
                rule: 'email_or_mobile email_or_mobile_remote',
                onItemValidated: function(error, message, eleme) {


                }
            });

         }



        if($("#code-form").length>0){


            var _form = $("#code-form");

            var isEmail = _form.data("is-email");;
            var emailOrMobile = _form.data("email-or-mobi");
            var emailSendUrl=_form.data("email-send-url");


            if(isEmail==1){


                $.ajax({

                    type:'POST',
                    url:emailSendUrl,
                    data:JSON.stringify({'value':emailOrMobile}),
                     contentType: "application/json; charset=utf-8",
                    success:function(data){

                        if(data.success==1){
                             _form.find('p.text-info').html("一条包含验证码的邮件已发送到您邮箱："+emailOrMobile)
                        }
                        else{
                            _form.find('p.text-info').html("邮件发送失败，请稍后重试")
                        }
                    }

                })

            }



             validator = new Validator({
                element: '#code-form',
                onFormValidated: function(err, results, form) {
                    if (err == false) {
                        $('#code-form').find("[type=submit]").button('loading');
                    }

                }

            });


            //  通过邮箱找回密码
            if(isEmail==1){




                  validator.addItem({
                    element: '#email_code',
                    required: true,
                    rule: 'integer fixedLength{len:4} remote',
                    onItemValidated: function(error, message, eleme) {


                    }
                    });


            }
            // 通过手机找回密码
            else{


                  validator.addItem({
                    element: '#validate_code',
                    required: true,
                    display:'图片验证码',
                    rule: 'integer fixedLength{len:4} remote',
                    onItemValidated: function(error, message, eleme) {

                        if (error) {
                                $('.js-sms-send').addClass('disabled');
                            return;
                        } else {
                                $('.js-sms-send').removeClass('disabled');
                        }
                    }
                });



                  validator.addItem({
                    element: '#sms_code',
                    required: true,
                      display:'短信验证码',
                    rule: 'integer fixedLength{len:4} remote',
                    onItemValidated: function(error, message, eleme) {


                    }
                });



                _form.on('click','.js-sms-send',function(e){



                    var _this = $(this);

                    var url =_this.data("sms-url");



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


                      $.ajax({

                        type:'POST',
                        url:url,
                        data:JSON.stringify({'value':emailOrMobile}),
                         contentType: "application/json; charset=utf-8",
                        success:function(data){

                            if(data.success==1){


                                $('#js-time-left').html('60');
                                $('#js-fetch-btn-text').html('秒后重新获取');
                                Notify.success('发送短信成功');
                                $('.js-sms-send').addClass('disabled');
                                refreshTimeLeft();
                            }
                            else{

                                 Notify.danger(data.message);
                            }
                        }

                    })





                })


                $(".js-validate-code-ref").on('click',function(){


                    var _this = $(this);
                    var url = $(this).data('url');

                    _this.find('img')[0].src=url+"?t="+Math.random();


                 })



            }





        }




            if($("#reset-form").length>0){


                    var _form=$("#reset-form");

                   validator = new Validator({
                    element: _form,
                    autoSubmit: false,
                    onFormValidated: function(err, results, form) {

                        if (err) {
                            return false;
                        }
                         _form.find("[type=submit]").button('loading');

                        var url = _form.data("action");
                        var login_url = _form.data("login");


                        var pwd = $("#new-password").val();
                        var emailOrMobile = $("#emailOrMobile").val();



                        $.ajax({

                            type:'POST',
                            url:url,
                            data:JSON.stringify({'password':pwd,'email_phone':emailOrMobile}),
                             contentType: "application/json; charset=utf-8",
                            success:function(data){

                                if(data.success==1){
                                     Notify.success(data.message);
                                     window.setTimeout("location.href=login_url",3000);
                                }
                                else{
                                      Notify.danger(data.message);

                                }
                            }

                        });

                    }

                });


                validator.addItem({
                    element: '[name="password"]',
                    required: true,
                    display:'密码',
                    rule: 'minlength{min:5} maxlength{max:20}',
                    onItemValidated: function(error, message, eleme) {


                    }
                });

                validator.addItem({
                    element: '[name="password-confirmation"]',
                    required: true,
                    display:'确认密码',
                    rule: 'confirmation{target: "#new-password"}',
                    onItemValidated: function(error, message, eleme) {


                    }
                });





            }







    };

});