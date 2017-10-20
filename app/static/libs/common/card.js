define(function (require, exports, module) {

    if(!navigator.userAgent.match(/(iPhone|iPod|Android|ios|iPad)/i)){

        $("body").on("mouseenter",'.js-user-card', function () {


            var _this = $(this);
            var userId = _this.data('userId');
            var loadingHtml = '<div class="card-body"><div class="card-loader"><span class="loader-inner"><span></span><span></span><span></span></span> 名片加载中</div>';


            var contentHtml='<div id="user-card-%userId%" class="js-card-content" data-user-id="%userId%">'
                             +' <div class="card-header media-middle">'
                             +'   <div class="media">'
                             +'     <div class="media-left">'
                             +'       <div class="user-avatar">'
                             +'           <a  href="/user/%userId%" data-card-url="/user/%userId%/public/info" data-user-id="%userId%">'
                             +'             <img class="avatar-md" src="%userLogo%">'
                             +'           </a>'
                             +'       </div>'
                             +'     </div>'
                             +'     <div class="media-body">'
                             +'       <div class="title">'
                             +'             <a class="link-dark " href="/user/%userId%">%userName%</a>'
                              +'      </div>'
                              +'      <div class="content"> </div>'
                             +'     </div>'
                             +'   </div>'
                             +'     <div class="metas">'
                             +'       <a class="btn btn-primary btn-xs follow-btn" href="javascript:;" data-url="/user/%userId%/follow" data-status-url="/user/%userId%/follow/status"  >关注</a>'
                             +'       <a class="btn btn-default btn-xs unfollow-btn" href="javascript:;"  data-url="/user/%userId%/unfollow" style="display:none;">已关注</a>'
                             +'       <a class="btn btn-default btn-xs js-send-message" herf="javascript:;" data-user-head="%userLogo%" >私信</a>'
                             +'     </div>'
                             +'     </div>'
                             +'   <div class="card-body">'
                              +'        %userDesc%'
                              +'    </div>'
                             +' <div class="card-footer clearfix">'
                             +'   <span><a class="link-light" >%courseCount%<br>在学</a></span>'
                             +'   <span><a class="link-light" href="/user/%userId%">%threadCount%<br>文章</a></span>'
                             +'   <span><a class="link-light" href="/user/%userId%/following">%followed%<br>关注</a></span>'
                             +'   <span><a class="link-light" href="/user/%userId%/followers">%followers%<br>粉丝</a></span>'
                             +' </div>'

                            +'</div>';




            var timer = setTimeout(function(){

                function callback(data) {

                    var headImgUrl = data.user_logo;

                    if(headImgUrl=='' || headImgUrl==null){
                        headImgUrl='/static/images/head_defualt.jpg'
                    }
                    var html =contentHtml.replace(new RegExp("%userId%",'gm'),data.user_id)
                    html =html.replace(new RegExp("%userName%",'gm'),data.user_name)
                    html =html.replace(new RegExp("%userLogo%",'gm'),headImgUrl)
                    html =html.replace("%followers%",data.followers)
                    html =html.replace("%followed%",data.followed)
                    html =html.replace("%courseCount%",data.study_course_count)
                    html =html.replace("%threadCount%",data.thread_count)
                    html =html.replace("%userDesc%",(data.user_desc==''||data.user_desc==null)?'暂无简介':data.user_desc)


                    _this.popover('destroy');


                    if ($('#user-card-' + userId).length == 0) {
                        if ($('body').find('#user-card-store').length > 0 ) {
                            $('#user-card-store').append(html);
                        } else {
                            $('body').append('<div id="user-card-store" class="hidden"></div>');
                            $('#user-card-store').append(html);
                        }
                    }



                    _this.popover({
                        trigger: 'manual',
                        placement: 'auto top',
                        html: 'true',
                        content: function(){
                            return html;
                        },
                        template: '<div class="popover cniao-card"><div class="arrow"></div><div class="popover-content"></div></div>',
                        container: 'body',
                        animation: true
                    });

                    _this.popover("show");

                    _this.data('popover', true);

                    $(".popover").on("mouseleave", function () {
                        $(_this).popover('hide');
                    });

                };

                if ($('#user-card-' + userId).length == 0 || !_this.data('popover')) {

                    function beforeSend () {

                        _this.popover({
                            trigger: 'manual',
                            placement: 'auto top',
                            html: 'true',
                            content: function(){
                                return loadingHtml;
                            },
                            template: '<div class="popover cniao-card"><div class="arrow"></div><div class="popover-content"></div></div>',
                            container: 'body',
                            animation: true
                        });

                        // _this.popover("show");

                    };

                    $.ajax ({
                        type:"GET",
                        url: _this.data('cardUrl'),
                        dataType: "json",
                        beforeSend: beforeSend,
                        success: callback
                    });


                    var is_login=($("meta[name='is-login']").attr("content")==1?true:false);

                    if(is_login){


                            var statusCheckUrl = "/user/"+userId+"/follow/status";

                            $.get(statusCheckUrl,function(data){

                                if(data.success){
                                 var $btn = $(".follow-btn");
                                 $btn.hide();
                                 $btn.siblings('.unfollow-btn').show();
                                }
                            })
                        }

                } else {
                    //var html = $('#user-card-' + userId).clone();
                     _this.popover("show");
                }


            },300);

            _this.data('timerId', timer);

        }).on("mouseleave",'.js-user-card', function () {

            var _this = $(this);

            setTimeout(function () {

                if (!$(".popover:hover").length) {

                    _this.popover("hide");

                }

            }, 100);

            clearTimeout(_this.data('timerId'));

        });



    }




});