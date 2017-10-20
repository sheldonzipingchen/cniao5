define(function(require, exports, module) {

    var Notify = require('common/bootstrap-notify');
//    var VideoJS = require('video-js');
    require("video-player");
//    require('gallery2/video-js/4.2.1/video-js-custom.css')

    require("balloon-video-player/1.3.0/src/skin/video-js.css")
    require("balloon-video-player/1.3.0/src/skin/pluck.css")


    var Widget = require('widget');


    var NormalVideoPlayer = Widget.extend({
    	attrs: {
        	hasPlayerError: false,
        	url: '',
            starttime: '0',
            timelimit: '10'
        },

        events: {

        },

        setup: function() {


            var techOrder = ['flash','html5'];
            if(this.get("agentInWhiteList")) {
                techOrder = ['html5', 'flash'];
            }

    		var that = this;


            videojs.options.flash.flashVars = {
                hls_debug: false,
                hls_debug2: false,
                hls_seekmode: "ACCURATE"
            };


            var plugins = {};


            var fingerprint = that.get('fingerprint');

             if(fingerprint != '') {

                    plugins = $.extend(plugins, {
                        fingerprint: {
                            html: fingerprint,
                            duration: 5000
                        }
                    })
                }




            var player = videojs(this.element.attr("id"), {
                    techOrder: ["flash", "html5"],
                    controls: true,
                    autoplay: true,
                    preload: 'none',
                    starttime: this.get('starttime'),
                    language: 'zh-CN',
                    width:'100%',
                    height:'100%',
                    plugins: plugins
                });

			player.dimensions('100%', '100%');
			player.src(this.get("url"));

			player.on('error', function(error){
			    that.set("hasPlayerError", true);
			    var message = '您的浏览器不能播放当前视频。';
			    Notify.danger(message, 60);
			});

			player.on('fullscreenchange', function(e) {
			    if ($(e.target).hasClass('vjs-fullscreen')) {
			        $("#site-navbar").hide();
			    }
			});

            // 播放结束
			player.on('ended', function(e){
                that._onEnded(e);
				that.trigger('ended', e);
			});

			player.on('timeupdate', function(e){
				that.trigger('timechange', e);

                 var currentTime = player.currentTime();
                 var timelimit = that.get('timelimit');
//                console.log("timelimit=="+timelimit)

                    if(timelimit>0 && timelimit<currentTime){
                        that.isPlaying() && player.pause();
                        player.currentTime(timelimit);
                        player.pause()
//                        player.pluck({
//                            text: "免费试看结束，购买后可完整观看",
//                            display:true
//                        });

                        Notify.success('免费试看结束，购买后可完整观看',10)
                    }
			});

			player.on('loadedmetadata' ,function(e){
				that.trigger('ready', e);
			});

            player.on("play", function(e){
                that.trigger("playing", e);
            });

            player.on("pause", function(e){
                that.trigger("paused", e);
            });

			this.set("player", player);

			NormalVideoPlayer.superclass.setup.call(this);
    	},

        checkHtml5: function() {
            if (window.applicationCache) {
                return true;
            } else {
                return false;
            }
        },

    	play: function(){
    		this.get("player").play();
    	},
        pause:function () {
            var player = this.get("player");
             player.pause();
        },

        _onEnded: function(e) {
        	if (this.get("hasPlayerError")) {
		        return ;
		    }
		    var player = this.get("player");

		    player.currentTime(0);
		    player.pause();
        },



        getCurrentTime: function() {
        	return this.get("player").currentTime();
        },

        getDuration: function() {
        	return this.get("player").duration();
        },

        setCurrentTime: function(time) {
			this.get("player").currentTime(time);
        },

        isPlaying: function() {

        	return !this.get("player").paused();
        },

        destroy: function() {
        	this.get("player").dispose();
        }
    });

    module.exports = NormalVideoPlayer;

});