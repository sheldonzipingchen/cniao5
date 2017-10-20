


define(function(require, exports, module) {

    window.$ = window.jQuery = require('jquery');
    require('bootstrap');
    require('common/bootstrap-modal-hack2');
    require("placeholder");

    require('message-sender');
    require('common/card');
    require('pace');
    require('pace-css-shop');


    var Swiper=require('swiper');


    exports.load = function(name) {

        seajs.use(name, function(module) {
            if ($.isFunction(module.run)) {
                module.run();
            }
        });

    };



    exports.loadScript = function(scripts) {
        for(var index in scripts) {
            exports.load(scripts[index]);
        }

    }

    window.app.load = exports.load;

    if (app.global_script) {
        exports.load(app.global_script);
    }

    if (app.controller) {
        exports.load(app.controller);
    }

    if (app.scripts) {
        exports.loadScript(app.scripts);
    }


    if ($('html').hasClass('lt-ie8')) {
        var message = '<div class="alert alert-warning" style="margin-bottom:0;text-align:center;">';
        message += '由于您的浏览器版本太低，将无法正常使用本站点，请使用最新的';
        message += '<a href="http://windows.microsoft.com/zh-CN/internet-explorer/downloads/ie" target="_blank">IE浏览器</a>、';
        message += '<a href="http://www.baidu.com/s?wd=%E8%B0%B7%E6%AD%8C%E6%B5%8F%E8%A7%88%E5%99%A8" target="_blank">谷歌浏览器</a><strong>(推荐)</strong>、';
        message += '<a href="http://firefox.com.cn/download/" target="_blank">Firefox浏览器</a>，访问本站。';
        message += '</div>';

        $('body').prepend(message);
    }




    $("i.hover-spin").mouseenter(function() {
        $(this).addClass("md-spin");
    }).mouseleave(function() {
        $(this).removeClass("md-spin");
    });




    if(!navigator.userAgent.match(/(iPhone|iPod|Android|ios|iPad)/i)){
        $("li.nav-hover").mouseenter(function(event) {
            $(this).addClass("open");
        }).mouseleave(function(event) {
            $(this).removeClass("open");
        });

    } else {
        $("body").on("click","li.nav-hover",function(){
//            $(this).toggleClass("open");
            $(this).addClass("abc"); // 不知道为什么随便加上个样式， $(this).toggleClass("open") 反而起作用

        })

        if ($(".nav-mobile li.nav-hover").is(":has(ul)")) {
            $(".nav-mobile li.nav-hover>a").attr("href","javascript:;");
        }
    }


    if ($('.cniao-wrap [data-toggle="tooltip"]').length > 0) {
        $('.cniao-wrap [data-toggle="tooltip"]').tooltip({container: 'body'});

    }

    $('[data-toggle="popover"]').popover();

    $(".js-search").focus(function () {
        $(this).prop("placeholder", "").addClass("active");
    }).blur(function () {
        $(this).prop("placeholder", "搜索").removeClass("active");
    });



     var is_login=($("meta[name='is-login']").attr("content")==1?true:false);

     if(is_login){

         $.get("/message/user/unread/count",function(data){

             var count = data.count;

             $("#message-count").html(count)
             if(count>0){

                 $(".nav.user-nav>li>a.hasmessage").append("<span class='dot'></span>")
             }

         })
     }

    $("body").on('click','#btn_login',function(){



        var _this=$(this);
        var go = _this.data("go");

        var cur_url = window.location.pathname


        window.location.href=go+"?next="+cur_url

    })




    var currUrl  =window.location.pathname

    var paths =currUrl.split("/");

    var currNav  = paths[1];
    $("#curr_nav2").find("li").removeClass("active")
    if(currNav=='' ){
        $("#nav-index").addClass("active")
    }else {

        if(currNav=="course"){

             if(paths[2] !=''){
                $("#curr_nav2").find("li").removeClass("active");
                 $("#nav-project").addClass("active")
            }
            else {

             $("#nav-course").addClass("active")
            }



        }
        // else  if(currNav=="vip"){
        //      $("#nav-project").addClass("active")
        //     $("#nav-"+currNav).addClass("active")
        // }
        else
            $("#nav-"+currNav).addClass("active")
    }





});


