define(function(require, exports, module) {
    var Notify = require('common/bootstrap-notify');
    var Validator = require('bootstrap.validator');

    require('common/validator-rules').inject(Validator);
    require('cniao-ckeditor');

     var Spin =require("spin")
    require('common/share');

    exports.run = function() {







        if($("#submit-thread-form").length>0){



            var $form = $("#submit-thread-form")

            var validator = new Validator({
                element: $form,
                failSilently: true,
                autoSubmit: false,
                onFormValidated: function(error) {
                    if (error) {
                        return false;
                    }
                    var btn= $('#submit-btn');
                    //btn.addClass('disabled');





                    var threadUrl = $('[name="thread[url]"]').val();


                    var reg ='http://www.cniao5.com/forum/thread/[0-9]{1,10}$';

                    var matchResult =threadUrl.match(reg)
                    if(!matchResult){

                        Notify.warning("只能是菜鸟窝下的文章,格式为http://www.cniao5.com/forum/thread/ID")
                        return false;

                    }


                    var arra =threadUrl.split("/")
                    var threadId =arra[arra.length-1]

                    var data={};
                    data.title=$('[name="thread[title]"]').val();
                    data.url=threadUrl
                    data.threadId=threadId;
                    data.forumId=$form.data("forum-id");




                    $.ajax({
                        'url':$form.data('url'),
                        'type':'post',
                        'data':JSON.stringify(data),
                         contentType: "application/json; charset=utf-8",
                         success: function(data) {

                           btn.removeClass('disabled');
                            if(data.success){

                                window.location.href=$form.data("go");
                            }
                            else{
                                Notify.danger(data.message);
                            }
                        },
                        'error': function(data) {
                            btn.removeClass('disabled');
                            Notify.danger('投稿失败，请重试');
                        }
                    });
                }
            });

            validator.addItem({
                element: '[name="thread[title]"]',
                required: true,
                rule: 'minlength{min:2} maxlength{max:100}',
                display:'标题'


            });
            validator.addItem({
                element: '[name="thread[url]"]',
                required: true,
                rule: 'url',
                display:'URL'

            });

        }


        if($("#thread-list").length>0){

            require("app/thread-list").run()
        }

        if($(".hot-threads").length>0){

            var eml =  $(".hot-threads");
            var url = eml.data("url");

            var spin = new Spin();
             spin.loading($("#course-list"))

            $.get(url,function(data){


                $(".hot-threads").setTemplateURL("/static/jtemplate/forum/hot-thread.html?d="+(+new Date()));
                $(".hot-threads").processTemplate(JSON.parse(data));

                spin.stop()

            });
        }




    };



});