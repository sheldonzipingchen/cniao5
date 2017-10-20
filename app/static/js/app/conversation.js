define(function(require, exports, module) {

    var Notify = require('common/bootstrap-notify');
     require('jquery.timeago');
    require('jquery.perfect-scrollbar')

    exports.run = function() {

        $(".timeago").timeago();


        var messageListEml = $("#message-list");

        var length = messageListEml.data('message-length');
        messageListEml.perfectScrollbar({minScrollbarLength:1});
        messageListEml.scrollTop((length-2)*80)

        messageListEml.perfectScrollbar("update");



        $.post($("#content-container").data("read-url"),function(data){

            console.log(data)
        })


        $('#message-reply-form').on('click', '#message-send-btn', function(e){



            $("#message-send-btn").addClass("disabled");

            if($("#message_reply_content").val().length >= 500){
                Notify.danger("不好意思，私信内容长度不能超过500!");
                return false;
            }

            if($.trim($("#message_reply_content").val()).length == 0){
                Notify.danger("不好意思，私信内容不允许为空!");
                return false;
            }

            var form = $("#message-reply-form");
            var data={};
            data.to_user_id=form.data("user-id");

            data.msg=$.trim($("#message_reply_content").val())



            $.ajax({
                    url:  "/message/user/message/send",
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                        $("#message-send-btn").removeClass("disabled");
                        if(data.success){

                            var current_user_id = form.data("current-user-id")
                            var current_user_logo = form.data("current-user-logo")

                            var date = new Date();//.Format("yyyy-MM-dd HH:mm:ss");

                            var html=' <li class="media message-me">'

                                       +' <a class="pull-right js-user-card"'
                                       +'    href="/user/'+current_user_id+'"'
                                       +'    data-card-url="/user/'+current_user_id+'/card/show"'
                                       +'    data-user-id="'+current_user_id+'">'
                                       +'          <img class="avatar-sm" src="'+current_user_logo+'">'
                                       +'   </a>'

                                        +'<div class="media-body">'
                                        +'<div class="popover left">'
                                        +'    <div class="arrow"></div>'
                                        +'    <div class="popover-content">'
                                        +'        <div class="message-content">'
                                        + $.trim($("#message_reply_content").val())
                                        +'        </div>'
                                        +'        <div class="message-footer">'
                                        +'            <span class="text-muted timeago" datetime ="'+date+'">'+date+'</span>'
                                         +'       </div>'
                                         +'   </div>'
                                      +'  </div>'
                                     +'   </div>'
                           +' </li>'

                            $(".message-list").append(html);
                            $("#message_reply_content").val("");

                            $(".timeago").timeago()
                        }
                        else{
                            Notify.warning(data.message);

                        }

                    },
                    error: function(data) {
                        $("#message-send-btn").removeClass("disabled");
                        Notify.danger('系统错误！');
                    }
                });

            return false;
        });

        $('.message-list').on('click', '.delete-message', function(e){

            if( $(".message-list").find(".message-me").length  == 1){
                if (!confirm('本条信息为最后一条，真的要删除该私信吗？')) {
                    return false;
                }
            } else {
                if (!confirm('真的要删除该私信吗？')) {
                    return false;
                }
            }

            var $item = $(this).parents('.media');
            $.post($(this).data('url'), function(data){

                //if($(".message-list").find(".message-me").length  == 1){
                //    window.location.href = $item.attr("parent-url");
                //}
                if(data.success)
                     $item.remove();
                else
                Notify.warning(data.message)
            });

        });


        $('textarea').bind('input propertychange', function() {
            if($("#message_reply_content").val().length > 1){
                $("#message-send-btn").removeClass("disabled");
            } else {
                $("#message-send-btn").addClass("disabled");
            }

        });

    };

});