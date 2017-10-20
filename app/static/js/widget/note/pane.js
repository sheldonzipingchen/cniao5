define(function(require, exports, module) {

    var wangEditor = require('wang-editor');
    var Notify = require('common/bootstrap-notify');

    var Widget = require('widget'),
    Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);

    var NotePane = Widget.extend({
        attrs: {
            editor: null,
            content: '',
            timer: null,
            plugin: null
        },
        events: {},
        setup: function() {},
        show: function() {
            this.get('plugin').toolbar.showPane(this.get('plugin').code);

            var pane = this,
                toolbar = pane.get('plugin').toolbar;

            $.get(pane.get('plugin').api.init, {
                courseId: toolbar.get('courseId'),
                lessonId: toolbar.get('lessonId')
            },
            function(html) {
                pane.element.html(html);

                var editorHeight = $("#lesson-note-plugin-form .note-content").height() - 50;


                var editor = new wangEditor({

                    element:'#note-editor-container',
                    editor_id:'note_content'
                }).render()

                pane.set('editor', editor);
                pane.set('content', editor.getHtml());


               var validator = new  Validator({
                    element: '#lesson-note-plugin-form',
                    failSilently: true,
                   autoSubmit:false,
                    onFormValidated: function(error) {
                        if (error) {
                            return false;
                        }
    //                    $('#groupthread-save-btn').button('submiting').addClass('disabled');


                          var content = editor.getHtml();

                    if(content.length <10){

                        Notify.danger('请再多写几个字吧')
                        return false
                    }

                    var data ={};
                    data.content=content;
                    data.course_id=toolbar.get('courseId');
                    data.lesson_id=toolbar.get('lessonId');
                    data.is_share =$("#share_note").val()


                       $.ajax({
                        url:  $(this).attr('action'),
                        data: JSON.stringify(data),
                        contentType: "application/json; charset=utf-8",
                        dataType:'json',
                        type:"POST",
                        success: function(result) {

                            Notify.success("笔记保存成功")
                            editor.clear()
                            pane.set('content', content);
                            pane.$('[data-role=saved-message]').html('已保存');
                            setTimeout(function(){
                                pane.$('[data-role=saved-message]').hide();
                            }, 3000);

                        },
                        error: function(data) {
                            console.log("error")
                        }
                       });

                    }
                  });

               validator.addItem({
                element: '[name="note[content]"]',
                required: true,
                display:'笔记',
                rule: 'minlength{min:10}'

            });

                $("#lesson-note-plugin-form").on('submit', function() {


                    pane.$('[data-role=saved-message]').html('正在保存').show();
                    //editor.updateElement();




                    return false;
                });

//                pane.autosave();
            });
        },

        autosave: function() {
            var pane = this;
            if (pane.get('timer')) {
                clearInterval(pane.get('timer'));
            };

            var timer = setInterval(function() {
                if (pane.get('editor').getHtml() != pane.get('content')) {
                    $("#lesson-note-plugin-form").trigger('submit');
                }
            }, 10000);

            pane.set('timer', timer);
        }
    });

    module.exports = NotePane;

});