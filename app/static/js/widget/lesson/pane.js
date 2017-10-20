define(function(require, exports, module) {

    var Widget = require('widget');

    require('jquery.perfect-scrollbar')
     require('template');
     require("layer");
    require("layer-css");

    var LessonPane = Widget.extend({

        _dataInitialized: false,

        attrs:{
            lessonCanPlay:false,
            courseCanPlay:false
        },

        setup: function() {


            var that = this,
                toolbar = this.get('toolbar');

            if (this._dataInitialized) {
                return;
            }

            var url = this.get('plugin').api.list
            url = url.replace('class_id',toolbar.get('courseId'))
            $.get(url,  function(data) {


               var can_play=toolbar.get('courseCanPlay') // 换成动态方式
               var new_data={}
               new_data.can_play = can_play;
               new_data.chatpers=data



                $(that.element).setTemplateURL("/static/jtemplate/lesson/lessons.html?d="+(+new Date()));
                $(that.element).processTemplate(new_data);

                that.element.show();
                that._setLessonItemActive(toolbar.get('lessonId'));
                var lessons = [];
                that.element.find('.lesson-item').each(function(index, item) {
                    var $item = $(item);
                    lessons.push(parseInt($item.data('id')));
                });
                toolbar.setLessons(lessons);

                var num=$('.lesson-item-'+toolbar.get('lessonId')).data('num')-5;
                $('.course-item-list-in-toolbar-pane').perfectScrollbar({wheelSpeed:20});
                $(".course-item-list-in-toolbar-pane").scrollTop(num*30);
                $(".course-item-list-in-toolbar-pane").perfectScrollbar('update');

            });

            toolbar.on('change:lessonId', function(lessonId) {
                that._setLessonItemActive(lessonId);
            });

            toolbar.on('learnStatusChange', function(data) {
                var $item = $("#course-item-list").find('.lesson-item-' + data.lessonId);
                var $itemStatusIcon = $item.find('.status-icon');
                var status = data.status == 'learning' ? 'doing' : 'done1';

                $itemStatusIcon.removeClass('es-icon-doing').removeClass('es-icon-done1')
                    .removeClass('es-icon-undone').removeClass('color-primary');
                $itemStatusIcon.addClass('color-primary').addClass('es-icon-'+status);
            });



            // 可是列表点击事件
            $("body").on("click",".js-lesson-item",function () {


                var $elm = $(this);


                var lesson_state = $elm.data("lesson-state");
                if(!lesson_state){
                    layer.msg("该课时暂时还未发布");
                    return;
                }

                var lesson_is_free=$elm.data('lesson-free');

                var lesson_id = $elm.data("lesson-id");
                var url = '/lesson/play/'+lesson_id+'.html'


                if(lesson_is_free){
                    that.openWindow(url,'lesson_p_',"_self")
                    return;
                }

                var can_play = $elm.data("can-play");

                if(can_play==0){

                    layer.open({
                         type: 1,
                         btn:[],
                        title:"喜欢就学吧",
                         area:['480px'],
                         offset:['100px'],
                         content:$("#dialog-buy")


                     });

                    return;
                }else
                {
                    that.openWindow(url,'lesson_p_',"_self")
                }


            })
        },

        show: function() {
            this.get('toolbar').showPane(this.get('plugin').code);
        },

        openWindow:function (url, emlId,openType) {

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

        },

        _setLessonItemActive: function(lessonId) {
            $("#course-item-list").find('.lesson-item').removeClass('item-active');
            $("#course-item-list").find('.lesson-item-' + lessonId).addClass('item-active');
        }
    });

    module.exports = LessonPane;

});