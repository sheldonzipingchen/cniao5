define(function(require, exports, module) {

      var Notify = require('common/bootstrap-notify');

      require('common/share');
      require('jquery.zclip');
      require('jbase64');


    var INVITE_DIRECT = "invite_direct";

    var shareUrl = "http://www.cniao5.com/invite/user/"

    var code ='';
    var title='［限时免费福利］菜鸟窝《Android高级工程师培训课程》、《React Native 零基础到高级》、《实战项目课程》、《VIP高级课程》现在免费学习啦。想学编程的小伙伴速来。时间有限.'

    exports.run = function() {

        var emlLink = $("#link-url")
        code = emlLink.data("code");

        emlLink.val(shareEncode(INVITE_DIRECT))

        $(".js-social-share-params").attr('data-url',shareEncode('sns'))
        $(".js-social-share-params").attr('data-message',title)




        $(".btn-login").on('click',function(){

            window.location.href = "/auth/login.html?next="+window.location.pathname

        })
        $(".btn-reg").on('click',function(){


            window.location.href = "/auth/reg.html?next="+window.location.pathname

        })



         $(".btn-copy").zclip({
                 path:'/static/libs/jquery/zclip/ZeroClipboard.swf',
                 copy:function(){

                     var url = shareEncode(INVITE_DIRECT)
                     return '［限时免费福利］菜鸟窝《Android高级工程师培训课程》、《React Native 零基础到高级》、《实战项目课程》、《VIP高级课程》现在免费学习啦。想学编程的小伙伴速来。时间有限：'+url
                 },
                 afterCopy: function(){
                     Notify.success("复制成功")
                 }

            });



        var emlUserName = $("#username");
        if (emlUserName.length>0){


            var username = emlUserName.data("name");

            if(username==null || username==''){
                Notify.warning("请先设置后用户名和头像再邀请好友");

                setTimeout(function(){

                    window.location.href='/member/setting/profile'
                },3000)
            }
        }

    };



    function shareEncode(channel){
 		params = 'from_code='+ code;
 		params = params+'&channel='+channel;
		params = base64_encode(params);
		makeUrl = shareUrl + params;
		return makeUrl;
 	}



});