
define(function(require, exports, module) {



    require("layer")
    require("layer-css")




     $(".js-search").on("click",function(){

        var this_=$(this);


         var href = this_.data("url");

         var q = $("#txt_query").val();
         if(q.length<=0){

             layer.msg("请输入订单号再查询");
             return
         }

         window.location.href = href +"&order_num="+q;


    })



     $(".js-update").on("click",function(){

        var this_=$(this);

        var oldVal=this_.data("val");
        var id = this_.data("id");

        var txtVal = $("#txt_val");
        txtVal.val(oldVal)

        layer.open({

            type:1,
            title:'修改',
            area:["400px"],
            offset: ['100px'],
            content:$("#dialog-modify"),
            btn:["确定"],
            yes:function(){

                var val = txtVal.val();

                if(val==""){

                    layer.msg("值不能为空");
                    return ;
                }


                var model ={}
                model.id = id;
                model.action=this_.data("action");
                model.val=val;

                post(model,this_.data('url'))




            }
        })

    })

    $(".js-update-status").on("click",function () {

         var this_=$(this);

         var val=this_.data("val");
         var id = this_.data("id");




        layer.confirm('您真的要取消该订单吗？',
            {
              btn: ['确认','关闭'] //按钮
            }, function(){

                 var model ={}
                model.id = id;
                model.action=this_.data("action");
                model.val=val;

                post(model,this_.data('url'))


            }, function(){

                layer.closeAll()

            });

    })


    function  post(model,url) {



                $.ajax({
                    url:  url,
                    data: JSON.stringify(model),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                       if (data.success){

                           window.location.reload();
                       }
                    },
                    error: function(data) {
                       layer.msg("系统出错")
                    }
                });
    }


});


