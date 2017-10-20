define(function(require, exports, module) {

    var Lazyload = require('echo.js');

    // var Spin =require("spin")
    // require('template');
    //require("jquery-esn-autobrowse")

    // var base_url ="/api/v1/course/pagination?";
    // var currentPage=1;
    // var pageSize=100;
    // var is_free=1000

    exports.run = function() {


       //  var FootAd = require('../widget/foot-ad')
       //
       //  FootAd = new FootAd({
       //     goUrl:'/hd/11.html?from=b-ad',
       //     adImgUrl:"http://cniao5-imgs.qiniudn.com/o_1b162ce0j18jr1mdu1mjg123t12m9.png"
       //
       // })

        Lazyload.init();


        // initCourse();
        //  $(".js-course-sort").on('click', function () {
        //
        //     var $this = $(this);
        //
        //     $(".js-course-sort").removeClass("active");
        //     $this.addClass('active');
        //
        //     initCourse()
        //
        // })

    //
    //    $(".course-list").autobrowse({
    //        url:function (offset) {
    //            //请求服务器端地址
    //
    //
    //                console.log("offset="+offset)
    //
    //                //var order_by = $(".js-course-sort.active").data("order-by");
    //                //if (order_by==undefined || order_by=='')
    //                //    order_by=0;
    //                //
    //                //var url=base_url+'is_free='+is_free + '&page_index='+offset+"&page_size="+pageSize+"&order_by="+order_by;
    //                //
    //                return 'http://baidu.com'
    //
    //
    //        }, template:function (data) {
    //            //异步组装服务器端返回的数据
    //
    //            //return parseData(data)
    //            return 'ffafafa'
    //        },
    //         itemsReturned:function (data) {
    //            //返回服务端数据的长度
    //
    //             return 10
    //        },
    //        offset:1,
    //        //max:10000,
    //        loader:'<div class="empty">正在加载</div>', //加载的图标,
    //        useCache:true, //使用缓存
    //        expiration:1,//过期时间
    //        sensitivity: 2000, //触发下一页的差值
    //        finished: function () { $(this).append('<p style="text-align:center">加载完成，没有更多课程了</p>') }//没有数据时的提示
    //});
    //
    //
    //

        // $('#free').on('click', function(event) {
        //
        //         var this_=$(this);
        //          is_free=this_.is(':checked')?1:1000;
        //         initCourse();
        // });
    };


    function initCourse(){

        var spin = new Spin();

        spin.loading($(".course-list"))

        var order_by = $(".js-course-sort.active").data("order-by");
        if (order_by==undefined || order_by=='')
            order_by=0;

        var url=base_url+'is_free='+is_free + '&page_index='+currentPage+"&page_size="+pageSize+"&order_by="+order_by

        $.get(url,function(data){

            parseData(data);

            spin.stop()

        })
    }



        function parseData(data){

            totalCount = data.totalCount;
            currentPage=data.pageIndex;

            if(totalCount<=0){

                var empty = "<div class='empty'>暂无数据</div>"
                 $(".course-list").append(empty);

                return
            }

            $(".course-list").setTemplateURL("/static/jtemplate/course/item.html?d="+(+new Date()));
            $(".course-list").processTemplate(data.datas);


         }




});