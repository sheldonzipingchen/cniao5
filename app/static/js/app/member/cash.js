define(function(require, exports, module) {




     require("layer")
     require("layer-css")
      require('common/share');
      require('jquery.zclip');
      require('jbase64');


     var  inviteCode = $(".js-invite-code").text();
     var  uniqueCode = $(".js-invite-code").data("unique-code");

    var  title = '菜鸟窝是一个高端技能学习平台,' +
        '有各种商业实战项目(直播,商城,聊天,音乐,团购,新闻,微博,手机助手 等),' +
        '热门技术 (ReactNative,Vue,RxJava,Dagger2,Retrofit 等),' +
        'HTML5项目实战 等高端课程。学习高端技术就来菜鸟窝。使用我的邀请码购买可以打折: '+inviteCode +"。 ";




    var url ='http://www.cniao5.com?';



    var message = title+shareEncode("cash-invite");

    exports.run = function() {


        $(".invite-code-input").val(message);

         $(".js-copy-one").zclip({
                 path:'/static/libs/jquery/zclip/ZeroClipboard.swf',
                 copy:function(){
                     return message;
                 },
                 afterCopy: function(){
                     layer.msg("复制成功!动动小手赚钱去吧")
                 }
            });


    };




    $(".js-social-share-params").attr('data-url',shareEncode("cash-invite")).attr('data-message',title)
    //




    function shareEncode(channel){
 		params = 'from_code='+ uniqueCode;
 		params = params+'&channel='+channel;
		params = base64_encode(params);
		makeUrl = url + params;
		return makeUrl;
 	}



});