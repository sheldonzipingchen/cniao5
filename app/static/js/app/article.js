define(function(require, exports, module) {
    var Notify = require('common/bootstrap-notify');
    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);
    require('cniao-ckeditor');

    function checkUrl(url) {
        var hrefArray = new Array();
        hrefArray = url.split('#');
        hrefArray = hrefArray[0].split('?');
        return hrefArray[1];
    }



    exports.run = function() {


//        if ($('#thread_content').length > 0) {
//            // group: group
//
//            var editor_thread = CKEDITOR.replace('thread_content', {
//                toolbar: 'Thread',
//                filebrowserImageUploadUrl: $('#thread_content').data('imageUploadUrl')
//            });
//
//
//            var validator_thread = new Validator({
//                element: '#user-thread-form',
//                failSilently: true,
//                onFormValidated: function(error) {
//                    if (error) {
//                        return false;
//                    }
//                    $('#groupthread-save-btn').button('submiting').addClass('disabled');
//                }
//            });
//
//            validator_thread.addItem({
//                element: '[name="thread[title]"]',
//                required: true,
//                rule: 'minlength{min:2} maxlength{max:200}',
//                errormessageUrl: '长度为2-200位'
//
//
//            });
//            validator_thread.addItem({
//                element: '[name="thread[content]"]',
//                required: true,
//                rule: 'minlength{min:2}'
//
//            });
//
//            validator_thread.on('formValidate', function(elemetn, event) {
//                editor_thread.updateElement();
//            });
//        }

        if ($('#post-thread-form').length > 0) {

            var editor = CKEDITOR.replace('post_content', {
                toolbar: 'Simple',

                filebrowserImageUploadUrl: $('#post_content').data('imageUploadUrl')
            });

            var validator_post_content = new Validator({
                element: '#post-thread-form',
                failSilently: true,
                autoSubmit: false,
                onFormValidated: function(error) {
                    if (error) {
                        return false;
                    }

                    $.ajax({
                        url: $("#post-thread-form").attr('post-url'),
                        data: $("#post-thread-form").serialize(),
                        cache: false,
                        async: false,
                        type: "POST",
                        dataType: 'text',
                        success: function(url) {
                            if (url) {
                                if (url == "/login") {
                                    window.location.href = url;
                                    return;
                                }
                                href = window.location.href;
                                var olderHref = checkUrl(href);
                                if (checkUrl(url) == olderHref) {
                                    window.location.reload();
                                } else {
                                    window.location.href = url;
                                }
                            } else {
                                window.location.reload();
                            }
                        },
                        error: function(data) {
                            data = data.responseText;
                            data = $.parseJSON(data);
                            if(data.error) {
                                Notify.danger(data.error.message);
                            } else {
                                Notify.danger('发表回复失败，请重试');
                            }
                        }
                    });
                }
            });
            validator_post_content.addItem({
                element: '[name="content"]',
                required: true,
                rule: 'minlength{min:2} visible_character'
            });

            validator_post_content.on('formValidate', function(elemetn, event) {
                editor.updateElement();
            });
        }




    };

});