
define(function(require, exports, module) {



    require("layer")
    require("layer-css")



    var wangEditor = require('wang-editor');

    var editor = new wangEditor({

            element:'#editor-container',
            editor_id:'goods_content'
        }).render()




    $("#btnSave").on("click",function () {

        var this_ = $(this);


        var content = editor.getHtml();

        var model ={}
        model.id = this_.data("id");
        model.action="content";
        model.val=content;


        $.ajax({
            url:  this_.data("post-url"),
            data: JSON.stringify(model),
            contentType: "application/json; charset=utf-8",
            dataType:'json',
            type:"POST",
            success: function(data) {
                layer.msg(data.message)

            },
            error: function(data) {
               layer.msg(data.message)
            }
        });





    })




});


