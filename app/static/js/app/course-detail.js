define(function(require, exports, module) {

    var Notify = require('common/bootstrap-notify');


    require('common/share');
    require('template');
    require('jquery.timeago');

    var Spin =require("spin")

    var FootAd = require('../widget/foot-ad')

    var class_id=0;
    var is_login=false
    exports.run = function() {



        //FootAd = new FootAd({
        //    goUrl:'http://www.cniao5.com/course/topic/pros?from=bottom_ad',
        //    adImgUrl:"http://cniao5-imgs.qiniudn.com/o_1aslm11hd14fk13p7ig61lle15fhe.png"
        //
        //})


          FootAd = new FootAd({
           goUrl:'/hd/12.html?from=b-ad',
           adImgUrl:"http://cniao5-imgs.qiniudn.com/o_1b3a25uau1iqovms1p6815li1u61e.png"

       })
       //    var FootAd = require('../widget/foot-ad')
       //
       //  FootAd = new FootAd({
       //     goUrl:'/hd/11.html?from=b-ad',
       //     adImgUrl:"http://cniao5-imgs.qiniudn.com/o_1b162ce0j18jr1mdu1mjg123t12m9.png"
       //
       // })



         is_login=($("meta[name='is-login']").attr("content")==1?true:false)

         class_id = $("#content-container").data("class-id");

           var btnBuy = $(".js-btn-buy");
            var btnTry = $(".js-btn-try");
            var btnLearn = $(".js-btn-learn");



        if ($(".course-header-top .actions").children().length>=3){

           $(".course-header-top .actions a").removeClass("btn-xlg").css({width:'30%','font-size':'16px','padding':'6px 10px'})
        }

        if(is_login){

            var auth_url = $("#content-container").data("class-auth-url");
            $.get(auth_url,function(data){


                var canPlay = data.can_play;
                var progress = data.progress;





                btnBuy.attr('data-course-auth',canPlay);
                $("#content-container").attr('data-course-auth',canPlay);

                // 有权限播放
                if(canPlay) {

                    btnBuy.addClass('hidden')
                    btnTry.addClass('hidden')

                    // 还没有开始学习
                    if(progress<=0)
                        btnLearn.removeClass('hidden')
                    else{
                         $(".cniao-section .progress").removeClass("hidden");
                         $(".cniao-section .course-header-bottom").removeClass("hidden");

                        var progressBar =  $(".cniao-section .progress .progress-bar");
                        var progress = parseInt( ((data.progress / data.total_lesson) * 100) );

                        progressBar.css('width',progress+'%');
                        progressBar.attr("title",progress+'%');
                        progressBar.attr("data-original-title",progress+'%');
                        $(".cniao-section .course-header-bottom .pull-left").html("完成课时： "+data.progress+" / "+data.total_lesson);

                        var current_lesson_Elm = $("#current_lesson_name");
                        current_lesson_Elm.text(data.current_name);
                        current_lesson_Elm.attr('data-lesson-id',data.current_id);

                        $(".js-btn-continue").attr('href','/lesson/play/'+data.current_id+".html")

                    }

                }
                else{
                    // 无权限播放
                     btnTry.removeClass('hidden')
                }

                //
                loadLessons(canPlay);
                loadCourseWare(canPlay);

            })

        }

        // 购买课程/开通会员按钮
        btnBuy.on('click',function(){

            var $btn=$(this);


            // 判断是否登录
            if(!is_login){
                window.location.href=$btn.data('loginurl');
                return;
            }

            buy_url = $btn.data("buy-url");

            window.location.href=buy_url

        })


        $(".js-btn-try").on('click',function(){


                var $btn=$(this);
                   // 判断是否登录
                if(!is_login){
                    window.location.href=$btn.data('loginurl');
                    return;

                }

              var url = "/lesson/play/try/"+class_id;

            $.ajax({
                url:url,
                async:false
            }).done(function(data){

                 if(data.success==0){
                      Notify.info("此课程还没有试学的课时",3000);
                      return
                  }

                  var lesson_id = data.lesson_id;

                  var play_url = "/lesson/play/"+lesson_id+".html"

                   openWindow(play_url,'lesson_p_2',"_blank")
            })




          })



        // 加载学习记录
        if($(".user-avatar-list").length>0){



            var spin = new Spin();
            var spin2 = new Spin();

            spin.loading($(".user-avatar-list-spinner"))
            spin2.loading($(".student-dynamic-list"))

             $.get('/api/v1/course/'+class_id+'/plays',function(data){


                 $("#play_count").html("( "+data.play_count +" )");

                  $(".user-avatar-list").setTemplateURL("/static/jtemplate/course/course_play_member.html?d="+(+new Date()));
                  $(".user-avatar-list").processTemplate(data.play_list);

                  $(".student-dynamic-list").setTemplateURL("/static/jtemplate/course/course_student_dynamic.html?d="+(+new Date()));
                  $(".student-dynamic-list").processTemplate(data.play_list);

                spin.stop()
                spin2.stop()
            })

        }


        // 加载课时
       loadLessons(false)

       // 加载源码课件
        loadCourseWare(false)


        // 加载评论
        if($("#evaluate-list").length>0){


            require('paginator')
             require('jquery.raty');
            var Validator = require('bootstrap.validator');



            var currentPage=1;
            var pageSize=10;
            var totalCount=0;

            initCommentData()


        Validator.addRule('star', /^[1-5]$/, '请打分');

        var $form = $('#review-form');

        if ($form.length > 0) {
            $form.find('.rating-btn').raty({
                path: $form.find('.rating-btn').data('imgPath'),
                hints: ['很差', '较差', '还行', '推荐', '力荐'],
                score: function() {
                    return $(this).attr('data-rating');
                },
                click: function(score, event) {
                    $form.find('[name=rating]').val(score);
                }
            });

            var validator = new Validator({
                element: $form,
                autoSubmit: false
            });

            validator.addItem({
                element: $form.find('[name=rating]'),
                required: true,
                rule: 'star',
                errormessageRequired: '请打分'
            });

            validator.addItem({
                element: $form.find('[name=content]'),
                required: true
            });


            validator.on('formValidated', function(error, msg, $form) {
                if (error) {
                    return;
                }


                if(!is_login){
                    Notify.danger("请登录后再评价");
                   return;
                }
               var auth =  $("#content-container").data('course-auth');

               if(!auth){
                   Notify.danger("抱歉，您不是该课程的学员，暂无权限评价此课程")
                   return
               }

                var data ={}
                data.course_id = class_id;
                data.score=$("#rating").val()
                data.content =$("#content").val()

                $('#comment-save-btn').button('submiting').addClass('disabled');
                    $.ajax({
                    url:  $form.data('url'),
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(result) {

                        $('#comment-save-btn').button('reset').removeClass('disabled');

                        if(result.success==1){
                            $("#content").val("")

                                $form.find('.text-success').fadeIn('fast', function(){
                                    initCommentData()
                                });
                        }else{
                            Notify.danger(result.message)
                        }

                    },
                    error: function(data) {
                        console.log("error")
                    }
                });


            });



            $('.js-hide-review-form').on('click', function(){
                $(this).hide();
                $('.js-show-review-form').show();
                $form.hide();
            });

            $('.js-show-review-form').on('click', function(){
                $(this).hide();
                $('.js-hide-review-form').show();
                $form.show();
            });

        }

        var $reviews = $('.js-reviews');

        $reviews.on('click', '.show-full-btn', function(){
            var $review = $(this).parents('.media');
            $review.find('.short-content').slideUp('fast', function(){
                $review.find('.full-content').slideDown('fast');
            });
            $(this).hide();
            $review.find('.show-short-btn').show();
        });

        $reviews.on('click', '.show-short-btn', function(){
            var $review = $(this).parents('.media');
            $review.find('.full-content').slideUp('fast', function(){
                $review.find('.short-content').slideDown('fast');
            });
            $(this).hide();
            $review.find('.show-full-btn').show();
        });



       function initCommentData(){



                var base_url ="/api/v1/course/comments/pagination?"
                var url=base_url+'class_id='+class_id+'&page_index='+currentPage+"&page_size="+pageSize

                var spin = new Spin();
                spin.loading($("#js-comments"))
                $.get(url,function(data){

                    parseData(data);
                    initPaginator();

                    $("#comment_count").html(data.totalCount)

                    spin.stop()

                })


            }

       function parseData(data){

                 totalCount = data.totalCount;
                 currentPage=data.pageIndex;


                $("#js-comments").setTemplateURL("/static/jtemplate/course/course-comments.html?d="+(+new Date()));
                $("#js-comments").processTemplate(data.datas);

                $(".timeago").timeago();
            }

       function initPaginator(){

              $('#pagination_comment').jqPaginator({
                       totalCounts:totalCount,
                       pageSize:pageSize,
                        visiblePages: 5,
                        currentPage: 1,
                        prev:'<li><a href="javascript:void(0)"><i class="icon icon-arrow-left3"></i></a></li>',
                        next:'<li><a href="javascript:void(0)"><i class="icon icon-arrow-right3"></i></a></li>',
                        page:'<li><a href="javascript:void(0)">{{page}}</a></li>',
                        onPageChange: function (num, type) {

                            if(type=='change'){

                                currentPage = num;

                                 var url=base_url+'class_id='+class_id+'&page_index='+currentPage+"&page_size="+pageSize;

                                  $.get(url,function(data){

                                    parseData(data);


                                })
                            }

                        }
                    });

            }

        }


        // 发表提问
        if($("#thread-form").length>0){

            require('app/thread-form.js').run()
        }


        // 提问列表

        var thread_list = $("#thread-list");

        if(thread_list.length>0){

             require('app/thread-list.js').run()
        }


        if($("#course-thread-detail").length>0){
             require('app/course-thread-detail').run()
        }


        $('[data-toggle="popover"]').popover();



    };


    function loadLessons(can_play){



        if($("#lesson-list").length>0){

            var chapterAnimate = require('widget/chapter-animate');

            new chapterAnimate({
                'element': '.course-detail-content'
            });


            var spin = new Spin();
            spin.loading($("#lesson-list"))

            $.get('/api/v1/course/'+class_id+'/chapters',function(data){


                if(data.length >0){

                   var new_data={}
                   new_data.is_login = is_login;
                   new_data.can_play = can_play;
                   new_data.chatpers=data


                   $("#lesson-list").setTemplateURL("/static/jtemplate/course/course-chapters.html?d="+(+new Date()));
                   $("#lesson-list").processTemplate(new_data);


                    showLessonDuration();

                     $('.cniao-wrap [data-toggle="tooltip"]').tooltip({container: 'body'});

                    $('.js-lesson-item').on('click',function(){

                        var $elm = $(this);


                        var lesson_state = $elm.data("lesson-state");
                        if(!lesson_state){
                             Notify.warning("该课时暂时还未发布");
                            return;
                        }

                        var lesson_is_free=$elm.data('lesson-free');

                        var lesson_id = $elm.data("lesson-id");
                        var url = '/lesson/play/'+lesson_id+'.html'


                        if(lesson_is_free){
                            openWindow(url,'lesson_p_',"_blank")
                            return;
                        }

                        var can_play = $elm.data("can-play");

                        if(!can_play){
                            Notify.warning("您暂无权限学习此课时，请购买课程后再学习");
                            return;
                        }
                         openWindow(url,'lesson_p_',"_blank")


                    })

               }


            });
        }

    }



    function loadCourseWare(can_play){

          // 加载源码
        if($("#source-list").length>0){


             var spin = new Spin();
            spin.loading($("#source-list"))

            $.get('/api/v1/course/'+class_id+'/wares',function(data){

                $("#source-list").setTemplateURL("/static/jtemplate/course/course_ware.html?d="+(+new Date()));
                $("#source-list").setParam('can_play',can_play);
                $("#source-list").processTemplate(data);

                $(".js-dl").on('click',function(){

                    var elm = $(this);
                    var id = elm.data("course-id");
                    var can_download = elm.data("can-download");

                    if(!can_download){

                        Notify.warning("您暂无权限学习下载此课件，请购买课程后再下载");
                            return;
                    }

                    window.location='/course/courseware/download/'+id;

                })

            })

        }

    }




    function showLessonDuration(){

        $(".date").each(function(){

            var this_ =$(this);

            var duration = this_.data('duration');

            this_.html(formatSeconds(duration))

        })

    }

    function formatSeconds(value) {
                var theTime = parseInt(value);// 秒
                var theTime1 = 0;// 分
                var theTime2 = 0;// 小时
                if(theTime > 60) {
                    theTime1 = parseInt(theTime/60);
                    theTime = parseInt(theTime%60);
                        if(theTime1 > 60) {
                        theTime2 = parseInt(theTime1/60);
                        theTime1 = parseInt(theTime1%60);
                        }
                }
                    var result = ""+parseInt(theTime);
                     if(theTime<10){
                         result="0"+theTime
                     }
                    if(theTime1 > 0) {

                        if(theTime1<10)
                            result = "0"+parseInt(theTime1)+":"+result;
                        else
                            result = ""+parseInt(theTime1)+":"+result;
                    }

//                    if(theTime2 > 0) {
//                        result = ""+parseInt(theTime2)+":"+result;
//                    }
                return result;
            }



    function openWindow(url, emlId,openType) {
                  var a = document.createElement('a');
                  a.setAttribute('href', url);
                  a.setAttribute('target',openType);
                  a.setAttribute('id', emlId);
                  a.setAttribute('style','display:none')

                var span = "<span id ='"+emlId+"_span'>click</span>"
                a.innerHTML =span;

                  // 防止反复添加

              var aEml = document.getElementById(emlId)
              if(!aEml) {
                  document.body.appendChild(a);
              }else{
                  aEml.setAttribute('href', url);
              }

             $("#"+emlId+"_span").trigger('click');

            return false;
        }



});