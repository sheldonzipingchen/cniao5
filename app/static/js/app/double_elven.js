define(function(require, exports, module) {




    require("layer")
    require("layer-css")


    require('jquery.zclip');
    require('jbase64');


    var INVITE_DIRECT = "invite_direct";

    var shareUrl = "http://www.cniao5.com/hd/11.html?"

    var code ='';

    exports.run = function() {





        $('body').scrollspy({ target: '#scrollspy_mine' })

         var emlLink = $("#link-url")
        code = emlLink.data("code");

        emlLink.val(shareEncode(INVITE_DIRECT))




        $(".btn-reg").on('click',function(){

            window.location.href = "/auth/reg.html?next="+window.location.pathname

        })




         $(".btn-copy").zclip({
                 path:'/static/libs/jquery/zclip/ZeroClipboard.swf',
                 copy:function(){



                     var url = shareEncode(INVITE_DIRECT)
                     return '【High爆双11菜鸟节,全场课程3折起还送新书】实战项目(直播,商城,聊天,音乐,团购,新闻,微博,手机助手 等),2016热门技术 (RxJava,Dagger2,Retrofit 等) ,React-Native 跨平台,HTML5项目实战 等课程大优惠 一年仅此一次,时间有限哦：'+url
                 },
                 afterCopy: function(){

                     layer.msg("复制成功,快去分享到QQ群后领取优惠吧")
                 }

            });





    };



    function shareEncode(channel){
 		params = 'from_code='+ code;
 		params = params+'&channel='+channel;
		params = base64_encode(params);
		makeUrl = shareUrl + params;
		return makeUrl;
 	}





});