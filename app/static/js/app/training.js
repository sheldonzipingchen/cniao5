define(function(require, exports, module) {


    var Notify = require('common/bootstrap-notify');
     require('common/share');



        require('jquery/radialIndicator/radialIndicator.min')
        require('jquery/radialIndicator/radialindicator.css')

        require('jquery/tipbox/jquery.tip.box')
        require('jquery/tipbox/animate.css')

        require("jquery-blurr");



    exports.run = function() {


     $(".train-header").blurr({height:200});

        is_login =($("meta[name='is-login']").attr("content")==1?true:false);



        $(".js-course-item").on('click',function(){


            var _this = $(this);

            //var taskId = _this.data("task-id");
            var course_url = _this.data("course-url");
            window.open(course_url,'_blank')

        })


        $('.js-route-panel').on('click', '.title', function(e){

             var _this = $(this);
             var mediaWrap = _this.parents('.step-item').find('.step-medias-wrap');

             mediaWrap.animate({
                visibility: 'toggle',
                opacity: 'toggle',
                easing: 'linear'
            });


        });


        $(".js-btn-join").on('click',function(){


            toLogin();

            var $this = $(this);


            var applyStatus = $this.data('apply-status');


            var is_open = $this.data('is-open');

            if (!is_open && applyStatus!=1){

               $("#class-dialog").modal('show')
                return
            }


            var checkUrl = $this.data('user-check-url');

            if (checkUrl !=''){

                $.ajax({
                  url: checkUrl,
                  success:function(data){

                      var info ='';

                        if(!data.email){
                            info="邮箱"
                        }

                        if(!data.mobi){
                            info=info+" 手机"
                        }
                        if(!data.qq){
                            info=info+" QQ"
                        }

                        if (info.length>0){
                            $("#btn-info").removeClass('hidden');
                            $("#btn-info").text( "完善 《"+info+"》");
                        }
                          if (!data.head){
                            $("#btn-head").removeClass('hidden');
                        }

                        if(info.length>0 || !data.head){
                             $("#tip-dialog").modal('show');
                         }
                        else
                        $("#join-tip-dialog").modal('show')

                  }
                })

             }






        })

        $("#btn-cfg-join-class").on('click',function(){

            var btn =$(this);

            var url = $(".js-btn-join").data("join-url");
            var class_id = $(".train-header").data("class-id")

            btn.button('submiting').addClass('disabled');

            var data={}
            data.class_id=class_id;

            $.ajax({
                url:  url,
                data: JSON.stringify(data),
                type:"POST",
                contentType: "application/json; charset=utf-8",
                success: function(data) {

                    //btn.button('reset').removeClass('disabled');

                    if(data.result){

                        Notify.success(data.message);

                        setTimeout( window.location.reload(),2000);

                    }
                    else{
                         Notify.danger(data.message);
                    }
                },
                error: function(data) {

                    btn.button('reset').removeClass('disabled');
                }
            });


        });


        $(".js-finish-task").on('click',function(){

            var _this = $(this);

            _this.addClass("disabled")

            $.get(_this.data("url"),function(data){

                if(data.result){

                   if(data.is_delay){ // 任务超时完成

                       Notify.success("因为你超时完成任务,所以无法获取 <strong class='color-danger'>"+data.return_course_credit+"</strong> 学分",5);
                    } else{
                        $.tipsBox({
                            obj: _this,
                            str: "学分+" + data.return_course_credit,
                            callback: function () {

                            }
                        });
                        niceIn(_this);


                       var creditNode =  $("#course_credit");
                       var credit = creditNode.text();
                       creditNode.text(parseInt(credit)+data.return_course_credit);
                    }


                    _this.text('已完成此任务');
                    $(".js-step-item"+ data.task_id).addClass('step-over');


                }
                else {
                    Notify.danger(data.message);
                     _this.removeClass("disabled");
                }

            });

        })


        if($("#study-progress").length>0){

            var statusUrl = $("#study-progress").data('status-check-url');

            $.get(statusUrl,function(data){


                data = JSON.parse(data);



                $(data).each(function(i,n){


                    var taskNode = $(".task"+ n.task_id);

                    console.log(taskNode)

                    taskNode.attr('data-learn-status',n.status);

                    // 正在学习
                    if(n.status ==1){

                        $(".js-finish-task"+n.task_id).removeClass('disabled');
                        $(".js-step-item"+ n.task_id).addClass('step-cur')
                    }
                    //完成任务
                    else if (n.status ==2){

                        $(".js-finish-task"+n.task_id).text('已完成此任务').removeClass("btn-warning").addClass('btn-success');
                        $(".js-step-item"+ n.task_id).addClass('step-over')
                    }
                    else if (n.status==3){

                        //taskNode.addClass('color-danger').text('超时完成').attr('data-original-title','超时完成');;
                        $(".js-step-item"+ n.task_id).addClass('step-over')
                         $(".js-finish-task"+n.task_id).text('超时完成此任务');
                         $(".js-finish-task"+n.task_id).addClass('disabled').removeClass("btn-warning");
                    }


                });

            })
        }


        if($("#finish-date").length>0){


            var infos= $("#study-progress");

            var start_time_str = infos.data('start-time');
            var learn_days = infos.data('total-days');

            var beginDate = new Date(start_time_str);

            beginDate.setDate(beginDate.getDate()+learn_days);

            $("#finish-date").text(beginDate.Format("yyyy-MM-dd"))


        }










    };




    function  toLogin(){
        if(!is_login){
                Notify.warning('请先登录!');
                setTimeout(function(){

                     window.location.href='/auth/login.html?next='+window.location

                },2000)
               return ;
        }
    }

    function niceIn(prop){
        prop.find('i').addClass('niceIn');
        setTimeout(function(){
            prop.find('i').removeClass('niceIn');
        },1000);
    }



    function  useTime(json){





        var now = new Date()
        var startTime = new Date(json.startTime)

        var times = now.getTime()-startTime.getTime()

        //计算出相差天数
        var days=Math.floor(times/(24*3600*1000))

        //计算出小时数

        var leave1=times%(24*3600*1000)    //计算天数后剩余的毫秒数
        var hours=Math.floor(leave1/(3600*1000))
//计算相差分钟数
        var leave2=leave1%(3600*1000)        //计算小时数后剩余的毫秒数
        var minutes=Math.floor(leave2/(60*1000))
//计算相差秒数
        var leave3=leave2%(60*1000)      //计算分钟数后剩余的毫秒数
        var seconds=Math.round(leave3/1000)


        return (days+"天"+hours+"小时"+minutes+"分")

    }

    function  getTotalMinutes(json){
        return json.taskDays * 24 * 60;
    }

    function  getInitMinutes(json){

        var now = new Date()
        var startTime = new Date(json.startTime)

        var times = now.getTime()-startTime.getTime()



        var minutes=Math.floor(times /1000 /60)

        return minutes

    }





    // 对Date的扩展，将 Date 转化为指定格式的String
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
// 例子：
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
Date.prototype.Format = function(fmt)
{ //author: meizz
  var o = {
    "M+" : this.getMonth()+1,                 //月份
    "d+" : this.getDate(),                    //日
    "h+" : this.getHours(),                   //小时
    "m+" : this.getMinutes(),                 //分
    "s+" : this.getSeconds(),                 //秒
    "q+" : Math.floor((this.getMonth()+3)/3), //季度
    "S"  : this.getMilliseconds()             //毫秒
  };
  if(/(y+)/.test(fmt))
    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
  for(var k in o)
    if(new RegExp("("+ k +")").test(fmt))
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
  return fmt;
}

});