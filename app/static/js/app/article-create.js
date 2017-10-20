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


        if ($('#thread_content').length > 0) {
            // group: group

            var editor_thread = CKEDITOR.replace('thread_content', {
                toolbar: 'Full',
                filebrowserImageUploadUrl: $('#thread_content').data('imageUploadUrl')
            });


            var validator_thread = new Validator({
                element: '#user-thread-form',
                failSilently: true,
                onFormValidated: function(error) {
                    if (error) {
                        return false;
                    }
                    $('#groupthread-save-btn').button('submiting').addClass('disabled');
                }
            });

            validator_thread.addItem({
                element: '[name="thread[title]"]',
                required: true,
                rule: 'minlength{min:2} maxlength{max:200}',
                errormessageUrl: '长度为2-200位'


            });
            validator_thread.addItem({
                element: '[name="thread[content]"]',
                required: true,
                rule: 'minlength{min:2}'

            });

            validator_thread.on('formValidate', function(elemetn, event) {
                editor_thread.updateElement();
            });
        }




    };

});