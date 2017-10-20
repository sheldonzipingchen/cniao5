
define(function(require, exports, module) {


    require("jquery-fancybox")
    require("jquery-fancybox-css")
    require("layer")
    require("layer-css")

    $(".fancybox").fancybox();


    $(".js-modify").on("click",function(){

        var this_=$(this);

        var oldVal=this_.data("val");
        var banner_id = this_.data("id");

        var txtVal = $("#txt_val");
        txtVal.attr("placeholder",oldVal)

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

                    layer.msg("请输入颜色值");
                    return ;
                }


                var model ={}
                model.id = banner_id;
                model.action=this_.data("action");
                model.val=val;

                $.ajax({
                    url:  this_.data('url'),
                    data: JSON.stringify(model),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                       if (data.success){

                            this_.html(txtVal.val());
                           layer.msg(data.message)
                           layer.closeAll();
                       }
                    },
                    error: function(data) {
                       layer.msg(data.message)
                    }
                });



            }
        })

    })

    $(".js-state").on("click",function(){

        var this_=$(this);

        var model ={}
        model.id = this_.data("id");
        model.action=this_.data("action");
        model.val=this_.data("val");


          $.ajax({
                    url:  this_.data('url'),
                    data: JSON.stringify(model),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                       if (data.success){
                           window.location.reload()
                       }
                    },
                    error: function(data) {
                       layer.msg(data.message)
                    }
                });


    })


        $(".js-delete").on("click",function(){

        var this_=$(this);

            layer.confirm('确认删除？', {
                      btn: ['删除','取消'] //按钮
                    }, function(){


                    var model ={}
                    model.id = this_.data("id");
                    model.action=this_.data("action");
                    model.val=this_.data("val");


                      $.ajax({
                                url:  this_.data('url'),
                                data: JSON.stringify(model),
                                contentType: "application/json; charset=utf-8",
                                dataType:'json',
                                type:"POST",
                                success: function(data) {

                                   if (data.success){
                                       window.location.reload()
                                   }
                                },
                                error: function(data) {
                                   layer.msg(data.message)
                                }
                            });


                    }, function(){

                        layer.closeAll()

                    });




    })






});


