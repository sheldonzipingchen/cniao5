define(function(require, exports, module) {


     var Notify = require('common/bootstrap-notify');
    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);
    require("placeholder");

    exports.run = function() {



        var $form =$("#form-give")

        var validator = new Validator({
            element: $form,
            autoSubmit: false,
            onFormValidated: function(error, results, $form) {

                if (error) {
                    return;
                }

                $('#btn-submit').button('submiting').addClass('disabled');

                var data={}

                var mobile = $("#user-phone").val()

                var coupon_id=$("#user-phone").data('coupon-id')

                data.mobile=mobile;
                data.coupon_id=coupon_id


                $.ajax({
                    url:  $form.data('post-url'),
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                        $('#btn-submit').button('reset').removeClass('disabled');

                        if (data.success) {
                            Notify.success('赠送成功！');
                            $("#give-dialog").modal('hide')
                            window.setTimeout('window.location.reload()',3000)

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
            element: '[name="user-phone"]',
            required: true,
            rule: 'mobile'
        });




        $('.give').on('click',function(){

            var $this = $(this)

            couponCode = $this.data('coupon-code')
            couponid = $this.data('coupon-id')

            $("#give-dialog").find(".coupon-code").html(couponCode);
            $("#user-phone").attr('data-coupon-id',couponid)

            $("#give-dialog").modal('show')

        })


    };

});