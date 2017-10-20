/**
 * Created by Ivan on 15/1/9.
 */

$(function(){

    /*$("#btn_login").click(function(){
        $('#modal_login').modal("show");

    });*/


    $(".user_head").popover({
        trigger:'manual',
        placement:"auto",
        template:'<div class="popover" role="tooltip"><div class="arrow" style="left: 30%"></div><div class="popover-content"></div></div>',
        html:true,

        content:function(){
            return $("#user_menu_panel").html();

        }


    }).on("mouseenter", function () {

            var _this = this;
            $(this).popover("show");
            $(this).siblings(".popover").on("mouseleave", function () {
                $(_this).popover('hide');
            });
        })
    .on("mouseleave", function () {

            var _this = this;
            setTimeout(function () {
                if (!$(".popover:hover").length) {
                    $(_this).popover("hide")
                }
            }, 100);
        });


    $("#txtQuery").on("focus",function(){

        $(".head_search_box").addClass("focus");
    }).on("blur",function(){

        $(".head_search_box").removeClass("focus");
    })





    $("#myTab a").click(function(e){

        $(this).tab('show');
    }).on('shown.bs.tab',function(e){

        $("#myTab a.cur").removeClass("cur");
        $(this).addClass("cur");

    });

    $("#tab_action a").click(function(e){

        $(this).tab('show');
    }).on('shown.bs.tab',function(e){

        $("#tab_action a.cur").removeClass("cur");
        $(this).addClass("cur");

    });







    $("#li_profile").click(function(){

        $("#a_profile").addClass("cur")
        $("#panel_profile").addClass("active");

        $("#a_change_pwd").removeClass("cur")
        $("#panel_change_pwd").removeClass("active");

    });


    $("#li_change_pwd").click(function(){

        $("#a_profile").removeClass("cur")
        $("#panel_profile").removeClass("active");

        $("#a_change_pwd").addClass("cur")
        $("#panel_change_pwd").addClass("active");

    });



    $("#li_course_learning").click(function(){

        $("#a_course_learning").addClass("cur")
        $("#panel_course_learning").addClass("active");

        $("#a_course_end").removeClass("cur")
        $("#panel_course_end").removeClass("active");

        $("#a_course_fav").removeClass("cur")
        $("#panel_course_fav").removeClass("active");

    });


    $("#li_course_end").click(function(){



        $("#a_course_end").addClass("cur")
        $("#panel_course_end").addClass("active");

        $("#a_course_fav").removeClass("cur")
        $("#panel_course_fav").removeClass("active");

         $("#a_course_learning").removeClass("cur")
        $("#panel_course_learning").removeClass("active");

    });


     $("#li_course_fav").click(function(){




        $("#a_course_fav").addClass("cur")
        $("#panel_course_fav").addClass("active");


        $("#a_course_end").removeClass("cur")
        $("#panel_course_end").removeClass("active");
         $("#a_course_learning").removeClass("cur")
        $("#panel_course_learning").removeClass("active");

    });








})



function secToMin(sec){

    // 计算
    var h=0,i=0,s=parseInt(sec);
    if(s>60){
        i=parseInt(s/60);
        s=parseInt(s%60);
        if(i > 60) {
            h=parseInt(i/60);
            i = parseInt(i%60);
        }
    }
    // 补零
    var zero=function(v){
        return (v>>0)<10?"0"+v:v;
    };

    var h = zero(h);
    if(h=='00')
        return  [zero(i),zero(s)].join(":");


    return [zero(h),zero(i),zero(s)].join(":");

}



//function secToMin(sec){
//
//    // 计算
//    var h=0,i=0,s=parseInt(sec);
//    if(s>60){
//        i=parseInt(s/60);
//        s=parseInt(s%60);
//        if(i > 60) {
//            h=parseInt(i/60);
//            i = parseInt(i%60);
//        }
//    }
//    // 补零
//    var zero=function(v){
//        return (v>>0)<10?"0"+v:v;
//    };
//    var res =  [zero(h),zero(i),zero(s)].join(":");
//
//    document.write(res)
//
////    return res;
//}



/**
*	手机号:目前全国有27种手机号段。&nbsp;
*	移动有16个号段：134、135、136、137、138、139、147、150、151、152、157、158、159、182、187、188。其中147、157、188是3G号段，其他都是2G号段。
*	联通有7种号段：130、131、132、155、156、185、186。其中186是3G（WCDMA）号段，其余为2G号段。
*	电信有4个号段：133、153、180、189。其中189是3G号段（CDMA2000），133号段主要用作无线网卡号。
*	150、151、152、153、155、156、157、158、159&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;九个&nbsp;
*	130、131、132、133、134、135、136、137、138、139&nbsp;&nbsp;&nbsp;&nbsp;十个&nbsp;
*	180、182、185、186、187、188、189&nbsp;&nbsp;&nbsp;七个&nbsp;
*	13、15、18三个号段共30个号段，154、181、183、184暂时没有，加上147共27个。&nbsp;&nbsp;
 *
 * /////
 * 1、最新的电话号码段：

移动：134(1349除外）135 136 137 138 139

147
150 151 152 157 158 159
182 183 184 187 188

联通： 130 131 132
155 156
185 186
145

电信：133 153 177 180 181 189
*/
function isMobiPhone(phone){
    var reg =/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;
	return reg.test(phone);
}

