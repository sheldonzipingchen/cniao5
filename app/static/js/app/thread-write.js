define(function(require, exports, module) {
    var Notify = require('common/bootstrap-notify');
    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);
    var wangEditor = require('wang-editor');

    require('jquery.perfect-scrollbar')
    require("highlight")
    require("highlight.css")


    exports.run = function() {



            hljs.initHighlightingOnLoad();
            $("#thread-write-content").perfectScrollbar({minScrollbarLength:1});



            $("body").on("click",'.cniao-checkbox',function(){

            var btn = $(this);

            btn.toggleClass("active")

            var className = btn.attr("class");
            if(className.indexOf("icon-checkbox-uncheck")>0){
                btn.addClass("icon-checkbox-checked2")
                btn.removeClass("icon-checkbox-uncheck")
            }
            else{
                btn.removeClass("icon-checkbox-checked2")
                btn.addClass("icon-checkbox-uncheck")
            }



        })

            //var editor_thread = CKEDITOR.replace('thread_content', {
            //    toolbar: 'Thread',
            //    height:'350px',
            //    allowedContent:true,
            //});


        var editor = new wangEditor({

            element:'#editor-container',
            editor_id:'thread_content'
        }).render()

        var $form = $("#thread-form")

        var action = $form.data("action");
        var url =action=='create'?$form.data('create-url'):$form.data("update-url");

        var validator_thread = new Validator({
            element: $form,
            failSilently: true,
            autoSubmit: false,
            onFormValidated: function(error) {
                if (error) {
                    return false;
                }
                var btn= $('#thread-save-btn');
                btn.addClass('disabled');



                var data={};
                data.content =editor.getHtml()
                data.title=$("#thread_title").val();
                data.thread_type=$form.data("thread-type")

                var brief = $("#thread_brief").val();

                if(brief=='' ||brief.length<=0){

                    brief  = editor.getFormatText()

                    if (brief.length>100){
                        brief = brief.substring(0,200);
                    }
                }

                data.brief = brief;
                data.is_original =0

                if($(".cniao-checkbox").attr("class").indexOf("active")>0){
                    data.is_original =1;
                }


                 if (action=='create')
                    data.forumId=$form.data("forum-id");
                 else if (action=='update')
                    data.threadId=$form.data("thread-id");



                $.ajax({
                    'url':url,
                    'type':'post',
                    'data':JSON.stringify(data),
                     contentType: "application/json; charset=utf-8",
                     success: function(data) {

                       btn.removeClass('disabled');
                        if(data.result){
                            Notify.success("发表成功！");
                            if(action=='create'){

                                editor.clear();
                                $("#thread_title").val('');
                                $("#thread_brief").val('');

                                $(".cniao-checkbox").removeClass("active");
                                $(".cniao-checkbox").removeClass("icon-checkbox-checked2");
                                $(".cniao-checkbox").addClass("icon-checkbox-uncheck");

                            }else{

                                var goUrl = '/forum/thread/'+$form.data("thread-id");
                                window.location.href=goUrl
                            }
                        }
                        else{
                            Notify.danger(data.message);
                        }
                    },
                    'error': function(data) {
                        btn.removeClass('disabled');
                        Notify.danger('发表失败，请重试');
                    }
                });
            }
        });

        validator_thread.addItem({
            element: '[name="thread[title]"]',
            required: true,
            rule: 'minlength{min:5} maxlength{max:180}',
            display:'标题'


        });
        validator_thread.addItem({
            element: '[name="thread[content]"]',
            required: true,
            rule: 'minlength{min:100}',
            display:'内容'

        });
        validator_thread.addItem({
            element: '[name="thread[brief]"]',
            rule: 'maxlength{max:200}',
            display:'摘要'

        });

        validator_thread.on('formValidate', function(elemetn, event) {
            //editor_thread.updateElement();
        });


    };

});