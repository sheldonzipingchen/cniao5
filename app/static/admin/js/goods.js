
define(function(require, exports, module) {



    require("layer")
    require("layer-css")

    require("bootstrap-switch/bootstrap-switch.min.css")
    require("bootstrap-switch/bootstrap-switch.min")




    $('.switch-checkbox').on('change', function(e) {


            var this_=$(this);

            var value = this_.is(':checked');

            var id = this_.data("id");
            var action = this_.data("action");
            var url = this_.data("url");


            var model ={}
            model.id = id;
            model.action=action;
            model.val=value==true?1:0;


            $.ajax({
                url:  url,
                data: JSON.stringify(model),
                contentType: "application/json; charset=utf-8",
                dataType:'json',
                type:"POST",
                success: function(data) {

                   if (!data.success){
                       layer.msg(data.message)
                   }

                },
                error: function(data) {
                   layer.msg(data.message)
                }
            });




        })



     $(".js-update").on("click",function(){

        var this_=$(this);

        var oldVal=this_.data("val");
        var course_id = this_.data("id");

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

                    layer.msg("值不能为空");
                    return ;
                }


                var model ={}
                model.id = course_id;
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
                           txtVal.val("");
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


});


