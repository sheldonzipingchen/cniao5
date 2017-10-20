define(function(require, exports, module) {

    var Lazyload = require('echo.js');
    require('common/service-block')
    var FootAd = require('../widget/foot-ad')

    exports.run = function() {
        Lazyload.init();


        $('[data-toggle="popover"]').popover();

     //FootAd = new FootAd({
     //       goUrl:'http://www.cniao5.com/forum/thread/3595?from=bottom_ad',
     //       adImgUrl:"http://7mno4h.com1.z0.glb.clouddn.com/footer_ad_android.png"
     //
     //   })
     //   FootAd = new FootAd({
     //       goUrl:'http://www.cniao5.com/course/topic/pros?from=bottom_ad',
     //       adImgUrl:"http://cniao5-imgs.qiniudn.com/o_1aslm11hd14fk13p7ig61lle15fhe.png"
     //
     //   })

        // FootAd = new FootAd({
        //    goUrl:'/hd/11.html?from=b-ad',
        //    adImgUrl:"http://cniao5-imgs.qiniudn.com/o_1b162ce0j18jr1mdu1mjg123t12m9.png"
        //
        // })

           FootAd = new FootAd({
           goUrl:'/hd/12.html?from=b-ad',
           adImgUrl:"http://cniao5-imgs.qiniudn.com/o_1b3a25uau1iqovms1p6815li1u61e.png"

       })


    };




});