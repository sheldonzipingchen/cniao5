define(function(require, exports, module) {

    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);
    require('cniao-ckeditor');

    var Notify = require('common/bootstrap-notify');

    exports.run = function() {

        // group: 'default'
        var editor = CKEDITOR.replace('thread_content', {
            toolbar: 'Thread'
//            filebrowserImageUploadUrl: $('#thread_content').data('imageUploadUrl')
        });


        var $form = $("#thread-form")
        var validator = new Validator({
            element:$form,
            failSilently: true,
            autoSubmit: false,
            onFormValidated: function(error) {
                    if (error) {
                        return false;
                    }


                var  is_login=($("meta[name='is-login']").attr("content")==1?true:false);

                if(!is_login){

                    Notify.danger("请先登录");
                    $("#btn-thread-save").removeAttr('disabled');
                    return false
                }

                var url = $form.data("url");
                var data ={};

                data.title = $("#thread_title").val();
                data.content = editor.getData();
                data.courseId=$("#content-container").data("class-id");

                console.log(JSON.stringify(data))
                 $.ajax({
                    url:  url,
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                        if (data.success) {

                            window.location.href=$form.data("go-url")
                        } else {

                            $("#btn-thread-save").removeAttr('disabled');
                            Notify.danger(data.message);
                        }
                    },
                    error: function(data) {
                         $("#btn-thread-save").removeAttr('disabled');
                        Notify.danger('系统错误！请稍候重试');
                    }
                });



               }
        });

        validator.addItem({
            element: '[name="thread[title]"]',
            required: true,
            rule:'visible_character'
        });

        validator.addItem({
            element: '[name="thread[content]"]',
            required: true
        });

        validator.on('formValidate', function(elemetn, event) {
            editor.updateElement();
        });

        validator.on('formValidated', function(err, msg, $form) {
            if (err == true) {
                return ;
            }

            $form.find('[type=submit]').attr('disabled', 'disabled');

            return true;
        });

    };

});