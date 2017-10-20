define(function(require, exports, module) {


    var Validator = require('bootstrap.validator');

    var Notify = require('common/bootstrap-notify');
    require('common/share');
    require('jquery.timeago');
    require("highlight")
    require("highlight.css")

    require('template');
    require('paginator')

    var Spin =require("spin")

    require('jquery/tipbox/jquery.tip.box')
    require('jquery/tipbox/animate.css')




    exports.run = function() {


        var  is_login=($("meta[name='is-login']").attr("content")==1?true:false);

        $(".timeago").timeago()
        hljs.initHighlightingOnLoad();
        $.get($("#content-container").data("read-url"),function(){})

        $('.author').on('click', '.delete', function(){
            var $btn = $(this);
            if (!confirm('真的要删除该文章吗？')) {
                return false;
            }

            $.post($btn.data('url'), function(data){

                if(data.success){

                    Notify.success("删除成功,2秒后关闭页面");
                    setTimeout(function(){
                        window.close()
                    },2000)
                }else{
                    Notify.danger(data.message)
                }

            });

        });

        if($(".js-thread-like").length>0 && is_login){

            var threadLikeEml = $('.js-thread-like');
            var url = threadLikeEml.data("url");

            $.get(url,function(data){

                    if(data.success){
                        threadLikeEml.addClass("liked")
                    }
                })


        }

        $(".like").on("click",'.like-button',function(){


                if(!is_login){
                    Notify.warning("请先登录");
                    return;
                }
                var btn = $(this);
                var parent = btn.parent();

                if(parent.attr('class').indexOf("liked")>0){
                    return;
                }

                var url = btn.data("url");

                $.post(url,function(data){


                    if(data.success){
                        var likeCount = btn.parent().find("#likes-count");

                         $.tipsBox({
                                    obj: btn,
                                    str: "喜欢+" + 1,
                                    callback: function () {
                                    }
                         })

                        var count = likeCount.html();
                        likeCount.html(parseInt(count)+1);

                        parent.addClass("liked")
                    }
                })

            })




        if($("#thread-post-list").length>0){

            require("app/thread-post").run();
        }


        if($(".top-courses").length>0){

            var eml = $(".top-courses");
            var userType = eml.data("user-type");
            var url = eml.data("learn-url");

            if(userType==2){
               url = eml.data("teach-url")
                eml.find("span.name").html("我教的课程")
            }
             var spin = new Spin();
             spin.loading($("#course-list"))

            $.get(url,function(data){

                $("#course-list").setTemplateURL("/static/jtemplate/course/course_item.html?d="+(+new Date()));
                $("#course-list").processTemplate(JSON.parse(data));

                spin.stop()
            })


        }

        if($(".latest-articles").length>0){


            var eml = $(".latest-articles");
            var url = eml.data("url");

              $.get(url,function(data){

                  data = JSON.parse(data);

                  $(data).each(function(index,thread){


                      var html=' <article> ' +
                          ' <div class="desc">' +
                                '<a class="title" href="/forum/thread/'+thread.id+'" target="_blank">'+thread.title+'</a>' +
                                '<div class="text-medium"><span class="mlm"> <i class="icon icon-zan"></i> '+thread.read_count+'</span> <span class="mlm"> <i class="icon icon-comment"></i> '+thread.reply_count+'</span></div>'+
                          '</div>' +
                          '</article>';

                      eml.append(html);

                  })
            })


        }




    };




});