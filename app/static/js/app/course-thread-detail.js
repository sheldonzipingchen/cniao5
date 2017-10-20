define(function(require, exports, module) {


    var Validator = require('bootstrap.validator');
    require('cniao-ckeditor');
    var Notify = require('common/bootstrap-notify');

    require('jquery.timeago');
    require("highlight")
    require("highlight.css")





    exports.run = function() {

        hljs.initHighlightingOnLoad();
        $.get($("#course-thread-detail").data("read-url"),function(){})

        require("app/thread-post").run();



        $('[data-role=confirm-btn]').click(function(){
            var $btn = $(this);
            if (!confirm($btn.data('confirmMessage'))) {
                return false;
            }
            $.post($btn.data('url'), function(){
                var url = $btn.data('afterUrl');
                if (url) {
                    window.location.href = url;
                } else {
                    window.location.reload();
                }
            });
        });




    };







});