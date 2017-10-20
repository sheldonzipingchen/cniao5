define(function(require, exports, module) {

    var Lazyload = require('echo.js');
    require('common/service-block')
    var FootAd = require('../widget/foot-ad')

    exports.run = function() {
        Lazyload.init();


        $('[data-toggle="popover"]').popover();

        // FootAd = new FootAd({
        //     goUrl:'/help/teacher/recruit.html',
        //     adImgUrl:"http://7mno4h.com1.z0.glb.clouddn.com/foot_ad_teacher.png"
        //
        // })

           FootAd = new FootAd({
           goUrl:'/hd/12.html?from=b-ad',
           adImgUrl:"http://cniao5-imgs.qiniudn.com/o_1b3a25uau1iqovms1p6815li1u61e.png"

       })
    };




});