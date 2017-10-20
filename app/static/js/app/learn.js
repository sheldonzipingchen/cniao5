define(function(require, exports, module) {


    var Widget = require('widget'),
        Class = require('class'),
        Store = require('store'),
        Notify = require('common/bootstrap-notify');

    var chapterAnimate = require('widget/chapter-animate');
    var Messenger = require('../widget/messenger');

    var Toolbar = require('../widget/lesson-toolbar');


    var iID = null;
    var LessonDashboard = Widget.extend({

        _router: null,
        _toolbar: null,
        _lessons: [],
        _counter: null,
        events: {
            'click [data-role=next-lesson]': 'onNextLesson',
            'click [data-role=prev-lesson]': 'onPrevLesson',
            'click [data-role=finish-lesson]': 'onFinishLesson',
            'click [data-role=ask-question]': 'onAskQuestion'
        },

        attrs: {
            courseId: null,
            courseUri: null,
            dashboardUri: null,
            lessonInfoUrl:null,
            lessonId: null,
            type: null,
            watchLimit: false,
            starttime: null,
            lessonCanPlay:false,
            courseCanPlay:false


        },

        setup: function() {
            this._readAttrsFromData();
            this._initToolbar();
            this._initLesson();
            this._initListeners();
            this._initChapter();


            $('.prev-lesson-btn, .next-lesson-btn').tooltip();
        },



        _readAttrsFromData: function() {

            this.set('courseId', this.element.data('courseId'));
            this.set('lessonId', this.element.data('lessonId'));
            this.set('lessonCanPlay', this.element.data('lesson-can-play'));
            this.set('courseCanPlay', this.element.data('course-can-play'));
            this.set('courseUri', this.element.data('courseUri'));
            this.set('dashboardUri', this.element.data('dashboardUri'));
            this.set('lessonInfoUrl',this.element.data('lesson-info-url'))
            this.set('watchLimit', this.element.data('watchLimit'));
            this.set('starttime', this.element.data('starttime'));
        },

        _initChapter: function(e) {
            this.chapterAnimate = new chapterAnimate({
                'element': this.element
            });
        },

        _initToolbar: function() {

            this._toolbar = new Toolbar({
                element: '#lesson-dashboard-toolbar',
                activePlugins: app.arguments.plugins,
                courseId: this.get('courseId'),
                lessonId:this.get("lessonId"),
                lessonCanPlay:this.get('lessonCanPlay'),
                courseCanPlay:this.get('courseCanPlay')
            }).render();

            $('#lesson-toolbar-primary li[data-plugin=lesson]').trigger('click');
        },


        _initListeners: function() {

            var that = this;
            this._toolbar.on('lessons_ready', function(lessons) {

                that._lessons = lessons;
                that._showOrHideNavBtn();

                if ($('.cniao-wrap [data-toggle="tooltip"]').length > 0) {
                    $('.cniao-wrap [data-toggle="tooltip"]').tooltip({
                        container: 'body'
                    });
                }
            });
        },

        _initLesson:function(){

            this._onChangeLessonId(this.get("lessonId"))
        },


        _initCounter: function(lessonId) {

            if (this._counter && this._counter.timerId) {
                clearInterval(this._counter.timerId);
            }

            var self = this;
            this._counter = new Counter(self, this.get('courseId'), lessonId, this.get('watchLimit'));

            this._counter.setTimerId(setInterval(function() {
                self._counter.execute()
            }, 1000));
        },

        _onChangeLessonId: function(id) {

            var self = this;

            if (!this._toolbar) {
                return;
            }
            this._toolbar.set('lessonId', id);

            $('#lesson-video-content').html("");

            this.element.find('[data-role=lesson-content]').hide();
            var that = this;



            $.get(this.get('lessonInfoUrl'), function(lesson) {


                that.set('type', lesson.type);
                that.element.find('[data-role=lesson-title]').html(lesson.title);


                var $titleStr = "";
                $titleArray = document.title.split(' - ');
                $.each($titleArray, function(key, val) {
                    $titleStr += val + ' - ';
                })
                document.title = lesson.title + ' - ' + $titleStr.substr(0, $titleStr.length - 3);



                if ((lesson.status != 1) && !/preview=1/.test(window.location.href)) {
                    $("#lesson-unpublished-content").show();
                    return;
                }


                var number = lesson.number - 1;

                if (lesson.canLearn == false) {

                    Notify.danger("您暂无权限学习该视频，请购买后再学习")
                    return;
                }


                 if (lesson.type == 'video' ) {

                    if (lesson.mediaSource == 'self') {
                        var lessonVideoDiv = $('#lesson-video-content');



                        var playerUrl = '/lesson/' + lesson.id + '/player';
                        if (self.get('starttime')) {
                            playerUrl += "?starttime=" + self.get('starttime');
                        }
                        var html = '<iframe src=\'' + playerUrl + '\' name=\'viewerIframe\' id=\'viewerIframe\' width=\'100%\'allowfullscreen webkitallowfullscreen height=\'100%\' style=\'border:0px\'></iframe>';

                        $("#lesson-video-content").show();
                        $("#lesson-video-content").html(html);

                        var messenger = new Messenger({
                            name: 'parent',
                            project: 'PlayerProject',
                            children: [document.getElementById('viewerIframe')],
                            type: 'parent'
                        });

                        messenger.on("ready", function() {

                        });

                        messenger.on("ended", function() {
                            var player = that.get("player");
                            player.playing = false;
                            that.set("player", player);

                            that._counter.finished=true;
                            that._onFinishLearnLesson();
                        });

                        messenger.on("playing", function() {

                            var player = that.get("player");
                            player.playing = true;
                            that.set("player", player);
                        });

                        messenger.on("paused", function() {
                            var player = that.get("player");
                            player.playing = false;
                            that.set("player", player);
                        });

                        messenger.on("timechange",function(data){

                            var player = that.get("player");
                            player.currTime = data.currTime;
                            that.set("player", player);
                        })

                        messenger.on("onMarkerReached", function(marker,questionId){

                        });
                        that.set("player", {});


                    }

                }


                that._toolbar.set('lesson', lesson);
                that._startLesson();

            });

            $.get('/lesson/' + id + '/learn/status', function(json) {

                var $finishButton = that.element.find('[data-role=finish-lesson]');
                if (json.status != 2) {
                    $finishButton.removeClass('btn-success');
                    $finishButton.attr('disabled', false);
                    $finishButton.find('.glyphicon').removeClass('glyphicon-check').addClass('glyphicon-unchecked');
                } else {
                    $finishButton.addClass('btn-success');
                    $finishButton.attr('disabled', true);
                    $finishButton.find('.glyphicon').removeClass('glyphicon-unchecked').addClass('glyphicon-check');
                }
            }, 'json');

            this._showOrHideNavBtn();

        },

        _showOrHideNavBtn: function() {
            var $prevBtn = this.$('[data-role=prev-lesson]'),
                $nextBtn = this.$('[data-role=next-lesson]'),
                index = $.inArray(parseInt(this.get('lessonId')), this._lessons);
            $prevBtn.show();
            $nextBtn.show();

            if (index < 0) {
                return;
            }

            if (index === 0) {
                $prevBtn.hide();
            } else if (index === (this._lessons.length - 1)) {
                $nextBtn.hide();
            }

        },

        _getNextLessonId: function(e) {

            var index = $.inArray(parseInt(this.get('lessonId')), this._lessons);
            if (index < 0) {
                return -1;
            }

            if (index + 1 >= this._lessons.length) {
                return -1;
            }

            return this._lessons[index + 1];
        },

        _getPrevLessonId: function(e) {
            var index = $.inArray(parseInt(this.get('lessonId')), this._lessons);
            if (index < 0) {
                return -1;
            }

            if (index == 0) {
                return -1;
            }

            return this._lessons[index - 1];
        },

        _startLesson: function() {

            var toolbar = this._toolbar,
                self = this;
            var url ='/lesson/learn/start';

            var data={};
            data.course_id = this.get('courseId');
            data.lesson_id = this.get('lessonId');


            $.ajax({
                    url:  url,
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(result) {

                        if (result.success == true) {
                            toolbar.trigger('learnStatusChange', {
                                lessonId: self.get('lessonId'),
                                status: 'learning'
                            });

                          self._initCounter(data.lesson_id);
                        }

                    },
                    error: function(data) {
                        console.log("error")
                    }
                });

        },

        _onFinishLearnLesson: function() {

            console.log("_onFinishLearnLesson")
            var $btn = this.element.find('[data-role=finish-lesson]'),
                toolbar = this._toolbar,
                self = this;

            var url = '/lesson/' + this.get('lessonId') + '/learn/finish';


               var data={};

//                data.currTime=player.currTime;
//                data.learningCount = learningCounter

                   $.ajax({
                    url:  url,
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(result) {

                        if (result.success) {


                            $btn.addClass('btn-success');
                            $btn.attr('disabled', true);
                            $btn.find('.glyphicon').removeClass('glyphicon-unchecked').addClass('glyphicon-check');
                            toolbar.trigger('learnStatusChange', {
                                lessonId: self.get('lessonId'),
                                status: 'finished'
                            });

                        }

                    },
                    error: function(data) {
                        console.log("error")
                    }
                });

        },

//        _onCancelLearnLesson: function() {
//             console.log("_onCancelLearnLesson")
//            var $btn = this.element.find('[data-role=finish-lesson]'),
//                toolbar = this._toolbar,
//                self = this;
//            var url = '../../course/' + this.get('courseId') + '/lesson/' + this.get('lessonId') + '/learn/cancel';
//
//            $.post(url, function(json) {
//                $btn.removeClass('btn-success');
//                $btn.find('.glyphicon').removeClass('glyphicon-check').addClass('glyphicon-unchecked');
//                toolbar.trigger('learnStatusChange', {
//                    lessonId: self.get('lessonId'),
//                    status: 'learning'
//                });
//            }, 'json');
//        },

        onNextLesson: function(e) {
            var next = this._getNextLessonId();
            if (next > 0) {

                window.location.href='/lesson/play/'+next+'.html'
            }
        },

        onPrevLesson: function(e) {

            var prev = this._getPrevLessonId();
            if (prev > 0) {
                 window.location.href='/lesson/play/'+prev+'.html'
            }
        },

        onFinishLesson: function(e) {
            var $btn = this.element.find('[data-role=finish-lesson]');
            if (!$btn.hasClass('btn-success')) {
                this._onFinishLearnLesson();
            }
        }


    });



    var Counter = Class.create({

        initialize: function(dashboard, courseId, lessonId, watchLimit) {
            this.dashboard = dashboard;
            this.courseId = courseId;
            this.lessonId = lessonId;
            this.interval =30;
//            this.watched = false;
            this.finished = false;
            this.watchLimit = watchLimit;
        },

        setTimerId: function(timerId) {
            this.timerId = timerId;
        },

        execute: function() {
//            var posted = this.addMediaPlayingCounter();
//            this.addLearningCounter(posted);
            this.addLearningCounter(true);
        },

        addLearningCounter: function(promptlyPost) {



            var learningCounter = Store.get("lesson_id_" + this.lessonId + "_learning_counter");
            if (!learningCounter) {
                learningCounter = 0;
            }


            var playing = this.dashboard.get("player").playing;

            if (playing !=true)
                return;

            learningCounter++;


            if (this.finished ||learningCounter >= this.interval) {

                var lesson_id = this.lessonId;


                var url = "/lesson/" + this.lessonId + '/learn/time' ;

                var player =  this.dashboard.get("player");


                var data={};

                data.currTime=player.currTime;
                data.learningCount = learningCounter

                   $.ajax({
                    url:  url,
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    async:false, // 在同步的情况下，使用Store.set 才生效
                    success: function(result) {

                        if(result.success==-1){
                            console.log("登录失效")
                            window.location.href='/auth/login.html?next=/lesson/play/'+lesson_id+".html";
                        }else {
                            learningCounter = 0;
                            Store.set("lesson_id_" + this.lessonId + "_learning_counter", learningCounter);
                        }

                    },
                    error: function(data) {
                        console.log("error")
                    }
                });


            }

            Store.set("lesson_id_" + this.lessonId + "_learning_counter", learningCounter);
        },

        addMediaPlayingCounter: function() {

            var mediaPlayingCounter = Store.get("lesson_id_" + this.lessonId + "_playing_counter");
            if (!mediaPlayingCounter) {
                mediaPlayingCounter = 0;
            }
            if (this.dashboard == undefined || this.dashboard.get("player") == undefined) {
                return;
            }


            var playing = this.dashboard.get("player").playing;
            var posted = false;


            if (mediaPlayingCounter >= this.interval || (mediaPlayingCounter > 0 && !playing)) {
                var url = "../../../../course/" + this.lessonId + '/watch/time/' + mediaPlayingCounter;
                var self = this;
                $.get(url, function(response) {
                    if (self.watchLimit && response.watchLimited) {
                        window.location.reload();
                    }
                }, 'json');
                posted = true;
                mediaPlayingCounter = 0;
            } else if (playing) {
                mediaPlayingCounter++;
            }

            Store.set("lesson_id_" + this.lessonId + "_playing_counter", mediaPlayingCounter);

            return posted;
        }
    });



    exports.run = function() {


        var is_login=($("meta[name='is-login']").attr("content")==1?true:false);
        if(!is_login){

            window.location.href='/auth/login.html'

        }



        var dashboard = new LessonDashboard({
            element: '#lesson-dashboard'
        }).render();


    };



});