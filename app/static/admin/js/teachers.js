
define(function(require, exports, module) {



    require("layer")
    require("layer-css")


    $(".js-jiesuang").on('click',function(){



        var this_ = $(this);

        var userId = this_.data("id");
        var balance = this_.data("balance");
        var username = this_.data("username");
        var bankName = this_.data("bank-name");
        var bankAccout = this_.data("bank-account");
        var getJiesuanMoneyUrl = this_.data("get-url");



        $("#teacherName").html(username)
        $("#balance").html(balance)
        $("#bankaccount").html(bankAccout)
        $("#bankname").html(bankName)


        $.get(getJiesuanMoneyUrl,function(data){

            $("#money").val(data.money);

        })



         layer.open({

            type:1,
            title:'费用结算',
            area:["600px"],
            offset: ['100px'],
            content:$("#jiesuang"),
             btn:['确认结算'],
             yes:function(){

                 var money = $("#money").val();
                 var model ={}
                model.user_id = userId;
                model.money=money;



                $.ajax({
                    url:  this_.data('post-url'),
                    data: JSON.stringify(model),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                       if (data.success){

                           //layer.msg(data.message)
                           //layer.closeAll();
                           window.location.reload()
                       }
                        else {
                            layer.msg(data.message)
                       }
                    },
                    error: function(data) {
                       layer.msg(data.message)
                    }
                });


             }

        });


    })
    $(".js-brief").on('click',function(){



        var this_ = $(this);

        var company = this_.data("company")
        var brief = this_.data("brief")


        var html="<div style='padding: 20px'> <div class='text-large gray-darker'> "+company+"</div>" +
            "<hr> <div class='text-sm'> "+brief+" </div></div>"

         layer.open({

            type:1,
            title:'讲师介绍',
            area:["500px"],
            content:html,


        })


    })





});


