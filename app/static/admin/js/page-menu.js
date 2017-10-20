
define(function(require, exports, module) {




    require("layer")
    require("layer-css")
    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);


    $("#btnAdd").on("click",function () {

         layer.open({

            type:1,
            title:'添加菜单',
            area:["600px"],
            offset: ['100px'],
            content:$("#addMenu")

        });


    })

    $(".js-delete").on("click",function () {


        var this_=$(this);


        layer.confirm('确认删除？', {
          btn: ['删除','取消'] //按钮
        }, function(){

             $.post(this_.data("url"),function (data) {

                 if (data.success){

                           layer.msg(data.message)
                           layer.closeAll();
                           window.location.reload()
                 }
                        else {
                            layer.msg(data.message)
                 }

            })


        }, function(){
           layer.closeAll()
        });



    })



         var $form = $("#form-add-menu");
         var validator = new Validator({
            element: $form,
            failSilently: true,
             autoSubmit: false,
            onFormValidated: function(error){


                if (error) {
                    return false;
                }


                 var title = $("#menu-title").val();
                 var redirectUrl = $("#menu-redirectUrl").val();
                 var sort = $("#menu-sort").val();

                 var model ={}
                 model.title = title;
                 model.redirect_url=redirectUrl;
                 model.sort=sort;


                $.ajax({
                    url:  $form.data('post-url'),
                    data: JSON.stringify(model),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                       if (data.success){

                           layer.msg(data.message)
                           layer.closeAll();
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

         validator.addItem({
                element: '#menu-redirectUrl',
                required: true,
                display:'跳转地址',


             });
         validator.addItem({
                    element: '#menu-title',
                    required: true,
                    display:'标题',

                 });

        validator.addItem({
                        element: '#menu-sort',
                        required: true,
                        rule: 'integer',
                        display:'排序'

                     });



});


