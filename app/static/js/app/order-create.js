define(function(require, exports, module) {

    require('placeholder');

    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);

        require("layer");
        require("layer-css");

      exports.run = function() {



          // 输入优惠码点击
        $("#coupon-code-btn").click(function(e){

            if(! isUseInvite()){
               showInput("coupon")
            }

        })


         // 使用优惠码点击
         $('button[role="coupon-use"]').click(function(e){

             if(isUseInvite()){
                 return;
             }

                var _this =$(this)
                var data={};
                var couponCode = $('[role="coupon-code-input"]');
                data.code = couponCode.val();
                if(data.code == ""){
                    $('[role="coupon-price-input"]').find("[role='price']").text("0.00");
                    return;
                }
                data.targetType = $("[name='product_type']").val();
                data.targetId = $("[name='product_id']").val();




                $.post('/member/coupon/user/'+data.targetType+'/'+data.targetId+'/check/'+data.code,  function(data){


                    $('[role="coupon-notify"]').css("display","inline-block");
                    if(data.success == false) {
                        $('[role=no-use-coupon-code]').show();
                        $('[role="coupon-notify"]').removeClass('alert-success').addClass("alert-danger").text(data.message);
                    } else if(data.success){
                        $('[role=no-use-coupon-code]').hide();
                        $('[role="coupon-notify"]').removeClass('alert-danger').addClass("alert-success").text("优惠码可用，您当前使用的是抵价"+data.decreaseAmount+"元的优惠码");
                        $('[role="coupon-price"]').find("[role='price']").text(moneyFormatFloor(data.decreaseAmount));
//                        $('[role="coupon-code-verified"]').val(couponCode.val());
                        $('[name="coupon_id"]').val(data.coupon_id);

                        $('[name="discount_type"]').val(1); // 优惠类型: 0 不使用优惠,1 使用优惠码 ,2 使用邀请码

                        _this.hide()
                        shouldPay('coupon');
                    }

                })
        })


          // 取消使用优惠码
         $('[role="cancel-coupon"]').click(function(e){


             cancelUse('coupon');
              $('[name="discount_type"]').val(0); // 优惠类型: 0 不使用优惠,1 使用优惠码 ,2 使用邀请码

         });



          //////////////////


             // 输入邀请码点击
        $("#invite-code-btn").click(function(e){


            if(!isUseCoupon()){
                showInput("invite");
            }


        })


          // 取消使用邀请码
         $('[role="cancel-invite"]').click(function(e){

             cancelUse('invite');
              $('[name="discount_type"]').val(0); // 优惠类型: 0 不使用优惠,1 使用优惠码 ,2 使用邀请码

         });



           // 使用邀请码点击
         $('button[role="invite-use"]').click(function(e){



             if(isUseCoupon()){
                 return;
             }


            var _this =$(this)
            var model={};
            var code = $('[role="invite-code-input"]');
            model.code = code.val();

            if(model.code == ""){
                $('[role="invite-price-input"]').find("[role='price']").text("0.00");
                return;
            }
            model.targetId = $("[name='product_id']").val();




            $.post('/member/invite/user/'+model.targetId+'/check/'+model.code,  function(data){


                $('[role="invite-notify"]').css("display","inline-block");
                if(data.success == false) {
                    $('[role=no-use-invite-code]').show();
                    $('[role="invite-notify"]').removeClass('alert-success').addClass("alert-danger").text(data.message);
                } else if(data.success){
                    $('[role=no-use-invite-code]').hide();

                    $('[role="invite-notify"]')
                        .removeClass('alert-danger')
                        .addClass("alert-success")
                        .html("您正在使用 <span style='color: red'>    "+data.username+"</span> 的邀请码,可以抵扣 "+data.decreaseAmount+"元");

                    $('[role="invite-price"]').find("[role='price']").text(moneyFormatFloor(data.decreaseAmount));

                    $('[name="invite_id"]').val(data.user_id);
                     $('[name="discount_type"]').val(2); // 优惠类型: 0 不使用优惠,1 使用优惠码 ,2 使用邀请码

                    _this.hide()
                    shouldPay('invite');
                }

            })
        })





      }



      function isUseInvite() {

            var isUseInvite = $('[name="invite_id"]').val()>0;
             if(isUseInvite){
                layer.msg("您已经使用邀请码,请先取消");
                 return true;
             }

             return false;

      }

      function isUseCoupon() {

           var isUseCoupon = $('[name="coupon_id"]').val() >0;

          if(isUseCoupon){
                layer.msg("您已经使用优惠码,请先取消");
                 return true;
             }

             return false;
      }

      function showInput(code_tag) {

           $('[role="'+code_tag+'-price"]').find("[role='price']").text("0.00");
            $('[role="'+code_tag+'-notify"]').text("").removeClass('alert-success');
            $('[role="'+code_tag+'-code"]').val("");
            $('[role="cancel-'+code_tag+'"]').hide();
            $('[role="'+code_tag+'-code-verified"]').val("");
            $('[role="'+code_tag+'-code-input"]').val("");
            $('[role="'+code_tag+'-code"]').show();
            $('[role="'+code_tag+'-code-input"]').focus();
            $('[role="cancel-'+code_tag+'"]').show();
            $('[role="null-'+code_tag+'-code"]').hide();

            $('#'+code_tag+'-code-btn').hide();
      }


      // 取消使用优惠码/邀请码
      function  cancelUse(code_tag) {



            $('[role="'+code_tag+'-code"]').hide();
            $("#"+code_tag+"-code-btn").show();
            $('[role="null-'+code_tag+'-code"]').show();
            $('button[role="'+code_tag+'-use"]').show()
            $('[role="no-use-'+code_tag+'-code"]').show()
            $('[role="'+code_tag+'-notify"]').hide();
            $('[role="'+code_tag+'-price"]').find("[role='price']").text("0.00");
            $('[role="'+code_tag+'-notify"]').text("");
            $('[role="'+code_tag+'-code"]').val("");

            $(this).hide();

            $('[role="cancel-'+code_tag+'"]').hide();

            $('[role="'+code_tag+'-code-verified"]').val("");
            $('[role="'+code_tag+'-code-input"]').val("");

             $('[name="'+code_tag+'_id"]').val(0);
            shouldPay(code_tag);
      }


       function moneyFormatFloor(value) {
        // 转化成字符串
        value = value + '';
        value = parseInt(Math.round(value * 1000));
        // 抹去最后１位
        value = parseInt(value/10) * 10 / 1000;
        return value.toFixed(2);
    }

    function shouldPay(tag){

         var totalPrice = parseFloat($('[name="total_price"]').val());

         var decreaseAmountInvite =parseFloat($('[role="invite-price"]').find("[role='price']").text());
         var decreaseAmountCoupon =parseFloat($('[role="coupon-price"]').find("[role='price']").text());

         var shoulpayMoney = totalPrice-decreaseAmountInvite-decreaseAmountCoupon;

         $("#shouldpay-money").text(moneyFormatFloor(shoulpayMoney))

    }


})