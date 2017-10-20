define(function(require, exports, module) {

    exports.run = function() {





       if($("#thread-list").length>0){

            require("app/thread-list").run()
        }


        var eml =$(".js-thread-query-params");

        var forumId = eml.data("target-id");

        $("#forum-"+forumId).addClass("active")





        require("layer");
        require("layer-css");

        $("#add-thead").on("click",function(){

             layer.open({
                 type: 1,
                 title:"抓取文章",
                 btn:[],
                 area:['600px'],
                 offset:['100px'],
                 content:$("#dialog-add-thread")


             });
        })

        $("body").on("click","#btn-save-task",function(){

                var btn =$(this);


                var url =$("#article_url").val();

                if(url==""){
                    layer.msg("请输入URL");
                    return
                }
                 var model ={};

                 model.site=$("#thread_site").val();
                 model.forum_id=$("#thread_forum_id").val();
                 model.url=url;



             $.ajax({
                url:  $("#thread-add-form").data('post-url'),
                data: JSON.stringify(model),
                contentType: "application/json; charset=utf-8",   ///普通表单提交注释, contentType
                dataType:'json',
                type:"POST",
                success: function(data) {

                    layer.msg("已添加爬虫任务");
                    $("#article_url").val("")

                },
                error: function(data) {

                    layer.msg("出错!!");
                }
            });


        })



    };



});