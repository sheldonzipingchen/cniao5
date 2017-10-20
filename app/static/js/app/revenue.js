define(function(require, exports, module) {

	var Notify = require('common/bootstrap-notify');
    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);

    exports.run = function() {


        var $form = $("#form-bind-alipay")
        var validator = new Validator({
            element: $form,
            failSilently: true,
             autoSubmit: false,
            onFormValidated: function(error){
                if (error) {
                    return false;
                }
                $('#bind-btn').button('submiting').addClass('disabled');


                 var data={}
                 data.alipay=$("#alipay").val()

                $.ajax({
                    url:  $form.data('post-url'),
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                        $('#bind-btn').button('reset').removeClass('disabled');

                        if (data.success) {
                            Notify.success('绑定成功！');
                            $("#alipay-dialog").modal('hide');
                            $("#withdrawal-dialog").modal('show')

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
            element: '#alipay',
             display:"支付宝账户",
            required: true,
            rule: 'minlength{min:4} maxlength{max:50}'
        });






         var $form_withdrawal = $("#form-withdrawal")

         var validator_withdrawal = new Validator({
            element: $form_withdrawal,
            failSilently: true,
             autoSubmit: false,
            onFormValidated: function(error){
                if (error) {
                    return false;
                }
                $('#withdrawal-btn').button('submiting').addClass('disabled');


                 var data={}
                 data.money=$("#money").val()

                $.ajax({
                    url:  $form_withdrawal.data('post-url'),
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                        $('#withdrawal-btn').button('reset').removeClass('disabled');

                        if (data.success) {
                            Notify.success('申请成功，3个工作日内会处理完成！');
                            $("#withdrawal-dialog").modal('hide')

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

        validator_withdrawal.addItem({
            element: '#money',
             display:"申请金额",
            required: true,
            rule: 'currency'
        });



        $(".balance-block").on('click', '.js-withdraw', function(){


            var $this = $(this);


            $.get($this.data("check-url"),function(data){

                if(!data.success){
                    Notify.danger('请先绑定支付宝账户');
                    $("#alipay-dialog").modal('show')
                }
                else{
                    $("#withdrawal-dialog").modal('show')
                }

            })



        });








    };

});