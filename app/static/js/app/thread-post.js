/**
 * Created by Ivan on 16/7/13.
 */

define(function(require, exports, module) {


    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);

    var Notify = require('common/bootstrap-notify');
    var Spin =require("spin")

    require('template');
    require('paginator');
    require('jquery.timeago');

     var wangEditor = require('wang-editor');




    var currentPage=1;
    var pageSize=10;
    var totalCount=0;
    var target_id =0;
    var target_type=''
    var base_url ="/api/v1/thread/post/pagination?"


    exports.run = function(){

        var $form = $("#thread-post-form");

        if ($form.length>0){


            var editor = new wangEditor({

                element:'#editor-container',
                editor_id:'post_content'
            }).render()


            var validator = new Validator({
                element: $form,
                failSilently: true,
                autoSubmit: false,
                onFormValidated: function(error){

                    if (error == true) {
                    return ;
                    }

                var  is_login=($("meta[name='is-login']").attr("content")==1?true:false);

                if(!is_login){

                    Notify.danger("请先登录");
                    $("#btn-thread-save").removeClass('disabled');
                    return false
                }

                $('.thread-post-list').find('li.empty').remove();



                var data={};
                data.content = editor.getHtml();
                data.courseId=$form.data("course-id");
                data.threadId=$form.data('thread-id');

                $.ajax({
                    'url':$form.data('post-url'),
                    'type':'post',
                    'data':JSON.stringify(data),
                     contentType: "application/json; charset=utf-8",
                    'success': function(data) {

                        $form.find('[type=submit]').removeClass('disabled');
                        if(data.success){

                            initPosts()

                            Notify.success("回复成功！");
                            editor.clear();
                        }
                        else{
                            Notify.danger(data.message);
                        }

                    },
                    'error': function(data) {
                        $form.find('[type=submit]').removeClass('disabled');
                        Notify.danger('发表回复失败，请重试');
                    }
                });

                 }
            });

            validator.addItem({
                element: '[name="post[content]"]',
                required: true,
                rule: 'minlength{min:3} maxlength{max:500}',
                display:'内容'
            });

            validator.on('formValidate', function(elemetn, event) {
                //editor.updateElement();
            });

        }



        var threadPostList = $("#thread-post-list");
        if(threadPostList.length>0){

            target_id = threadPostList.data("target-id")
            target_type = threadPostList.data("target-type")
            initPosts();


         $('#thread-post-list').on('click','.thread-post-action',function(){

            var userName=$(this).data('user');

            editor.append('@'+userName+'&nbsp;');

        });

         $("#thread-post-list").on('click', '.post-delete-btn', function() {
            if (!confirm("您真的要删除该回帖吗？")) {
                return false;
            }
            var $btn = $(this);
            $.post($btn.data('url'), function(){
                window.location.reload();
            });
        });

        }


    }




    function initPosts(){

        var spin = new Spin();
        spin.loading($("#thread-post-list"))

        var url=base_url+'target_id='+target_id+'&page_index='+currentPage+"&page_size="+pageSize+"&target_type=thread"


        $.get(url,function(data){


            parseData(data);
             spin.stop()


        })
    }

    function parseData(data){

                 totalCount = data.totalCount;
                 currentPage=data.pageIndex;

                if(totalCount<=0){

                     $("#thread-post-list").append("<li class='empty'>暂无数据<li>")
                    return
                }

                $("#thread-post-num").html(totalCount)

                if(target_type=='forum'){
                     $("#thread-post-list").setTemplateURL("/static/jtemplate/forum/thread-posts.html?d="+(+new Date()),null,{filter_data:false});
                     $("#thread-post-list").setParam("login_user",$("#thread-post-list").data("login-user-id"));
                }
                else
                    $("#thread-post-list").setTemplateURL("/static/jtemplate/course/course_thread_posts.html?d="+(+new Date()),null,{filter_data:false});

                $("#thread-post-list").processTemplate(data.datas);

               $(".timeago").timeago();
                initPaginator();
         }

    function initPaginator(){

              $('#pagination-thread-post').jqPaginator({
                       totalCounts:totalCount,
                       pageSize:pageSize,
                        visiblePages: 5,
                        currentPage: currentPage,
                        prev:'<li><a href="javascript:void(0)"><i class="icon icon-arrow-left3"></i></a></li>',
                        next:'<li><a href="javascript:void(0)"><i class="icon icon-arrow-right3"></i></a></li>',
                        page:'<li><a href="javascript:void(0)">{{page}}</a></li>',
                        onPageChange: function (num, type) {

                            if(type=='change'){

                                currentPage = num;

                                  var url=base_url+'target_id='+target_id+'&page_index='+currentPage+"&page_size="+pageSize+"&target_type=thread"

                                  $.get(url,function(data){

                                    parseData(data);


                                })
                            }

                        }
                    });

            }




})
