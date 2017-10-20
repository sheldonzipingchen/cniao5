define(function(require, exports, module) {

    var Lazyload = require('echo.js');

    var Swiper = require('swiper');

    var FootAd = require('../widget/foot-ad')

    // FootAd = new FootAd({
    //        goUrl:'http://www.cniao5.com/course/topic/pros?from=bottom_ad',
    //        adImgUrl:"http://cniao5-imgs.qiniudn.com/o_1b1606ge419svn1d1ncl1f5o1fen9.jpg"
    //
    //    })



       //   FootAd = new FootAd({
       //     goUrl:'/train/android',
       //     adImgUrl:"http://7mno4h.com1.z0.glb.clouddn.com/footer_ad_android.png"
       //
       // })

       //    FootAd = new FootAd({
       //     goUrl:'/hd/11.html?from=b-ad',
       //     adImgUrl:"http://cniao5-imgs.qiniudn.com/o_1b162ce0j18jr1mdu1mjg123t12m9.png"
       //
       // })
    //
      FootAd = new FootAd({
           goUrl:'/hd/12.html?from=b-ad',
           adImgUrl:"http://cniao5-imgs.qiniudn.com/o_1b3a25uau1iqovms1p6815li1u61e.png"

       })


    exports.run = function() {


        if ($(".cniao-poster .swiper-slide").length > 1) {

            var swiper = new Swiper('.cniao-poster.swiper-container', {
                pagination: '.swiper-pager',
                paginationClickable: true,
                autoplay: 5000,
                autoplayDisableOnInteraction: false,
                loop: true,
                calculateHeight: true,
                roundLengths: true,
                onInit: function(swiper) {
                    $(".swiper-slide").removeClass('swiper-hidden');
                }
            });
        }

        Lazyload.init();





        $(".teacher-item").mouseover(function(){



            var _this = $(this);

            var div_bottom = _this.children(".teacher-bottom");

            $(div_bottom).addClass("teacher-bottom-hover");
            $(div_bottom).css("height",$(div_bottom).children(".more").outerHeight());



        });
        $(".teacher-item").mouseleave(function(){


            var _this = $(this);

            var div_bottom = _this.children(".teacher-bottom");

            $(div_bottom).removeClass("teacher-bottom-hover");

            $(div_bottom).css("height","90px");

        })



        $('.recommend-teacher').on('click', '.teacher-item .follow-btn', function(){
            var $btn = $(this);
            var loggedin = $btn.data('loggedin');
            if(loggedin == "1"){
                showUnfollowBtn($btn);
            }
            $.post($btn.data('url'));
        }).on('click', '.teacher-item .unfollow-btn', function(){
            var $btn = $(this);
            showFollowBtn($btn);
            $.post($btn.data('url'));
        })
//
//
//        function showFollowBtn($btn)
//        {
//            $btn.hide();
//            $btn.siblings('.follow-btn').show();
//            $actualCard = $('#user-card-'+ $btn.closest('.js-card-content').data('userId'));
//            $actualCard.find('.unfollow-btn').hide();
//            $actualCard.find('.follow-btn').show();
//        }
//
//        function showUnfollowBtn($btn)
//        {
//            $btn.hide();
//            $btn.siblings('.unfollow-btn').show();
//            $actualCard = $('#user-card-'+ $btn.closest('.js-card-content').data('userId'));
//            $actualCard.find('.follow-btn').hide();
//            $actualCard.find('.unfollow-btn').show();
//        }

    };

});