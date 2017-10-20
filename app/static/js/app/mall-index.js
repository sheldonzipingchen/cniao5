define(function(require, exports, module) {



    exports.run = function() {



    require("layer");
    require("layer-css");

        if($(".js-buy").length>0){


            var Validator = require('bootstrap.validator');
            require('common/validator-rules').inject(Validator);

            var $form = $('#form-user-address-info');

            var validator = new Validator({
                element: $form,
                autoSubmit: false,
                onFormValidated: function(error, results, $form) {
                    if (error) {
                        return false;
                    }


                     $('#btnSave').button('submiting').addClass('disabled');

                    var model={};

                    model.real_name=$("#realname").val();
                    model.addr=$("#address").val();
                    model.mobi=$("#mobi").val();

                     layer.load();

                      $.ajax({
                        url:  $form.data('post-url'),
                        data: JSON.stringify(model),
                        contentType: "application/json; charset=utf-8",   ///普通表单提交注释, contentType
                        dataType:'json',
                        type:"POST",
                        success: function(data) {

                            $('#btnSave').button('reset').removeClass("disabled")
                            if(data.success){
                                layer.closeAll();

                                layer.msg("兑换成功");

                            }
                            else {
                                 layer.msg(data.message);
                            }
                        },
                        error: function(data) {
                            $('#btnSave').button('reset').removeClass("disabled")
                            layer.msg("系统错误,稍后重试");
                        }
                    });

                },
                failSilently: true
                });

            validator.addItem({
                element: '[name="profile[realname]"]',
                required: true,
                rule: 'chinese minlength{min:2} maxlength{max:12}'
            });

            validator.addItem({
            element: '[name="profile[addr]"]',
            required: true,
            rule: 'minlength{min:6} maxlength{max:50}'
        });
            validator.addItem({
            element: '[name="profile[mobile]"]',
                required: true,
            rule: 'mobile'
        });



        $(".js-buy").on("click",function(){


            var this_=$(this)

            var is_login=($("meta[name='is-login']").attr("content")==1?true:false);

            if(!is_login){

                layer.msg("请先登录");
                setTimeout(function(){
                    window.location.href="/auth/login.html?next="+window.location

                },2000)

                return;

            }

            var isVirtualGoods = this_.data("is-virtual");
            var price = this_.data("price");
            var userCoin = this_.data("user-coin");

            if(userCoin<price){

                showDialog("鸟币不足","modal-no-coin");
                return;
            }



            var buyUrl = this_.data("buy-url");

            $("#buy-goods").attr('data-url',buyUrl);
            $("#form-user-address-info").attr('data-post-url',buyUrl);

            $(".goods-coin").text(price)

            if(isVirtualGoods)
                showDialog("确认兑换","modal-buy-cfg");
            else{

                layer.open({
                 type: 1,
                 title:"确认兑换",
                 btn:[],
                 area:['600px'],
                 offset:['30px'],
                 content:$("#modal-buy2-cfg")


             });
            }



        })

        $("#buy-goods").on("click",function(){

            var this_=$(this)

            this_.addClass("disabled")
            var buyUrl = this_.data("url");
            layer.load();
            $.post(buyUrl,function(data){

                this_.removeClass("disabled")
                if(data.success){

                    layer.msg("兑换成功");
                    layer.closeAll();
                    setTimeout(function(){
                    window.location.href=this_.data("go-url")

                     },2000)
                }
                else {
                    layer.warning(data.message)
                }

            })

        })


         function showDialog(title,dialogID) {


          layer.open({
                 type: 1,
                 title:title,
                 btn:[],
                 area:['600px'],
                 offset:['100px'],
                 content:$("#"+dialogID)


             });
    }





     }





    };



});