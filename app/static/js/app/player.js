define(function(require, exports, module) {

    var Store = require('store');
    var Class = require('class');
    var Messenger = require('../widget/messenger');

    exports.run = function() {

        var videoHtml = $('#lesson-video-content');

        var userId = videoHtml.data("userId");
        var fileId = videoHtml.data("fileId");

        var courseId = videoHtml.data("courseId");
        var lessonId = videoHtml.data("lessonId");
        var timelimit = videoHtml.data('timelimit');

        var playerType = videoHtml.data('player');
        var fileType = videoHtml.data('fileType');
        var url = videoHtml.data('url');
        var token = videoHtml.data('tk');

        var watermark = videoHtml.data('watermark');
        var fingerprint = videoHtml.data('fingerprint');
        var fingerprintSrc = videoHtml.data('fingerprintSrc');
        var starttime = videoHtml.data('starttime');
        var agentInWhiteList = videoHtml.data('agentInWhiteList');



        var html = "";
        if(fileType == 'video'){
            if (playerType == 'normal-video'){
                html += '<video id="lesson-player" style="width: 100%;height: 100%;" class="video-js vjs-default-skin vjs-big-play-centered" controls preload="auto"></video>';
            } else {
                html += '<div id="lesson-player" style="width: 100%;height: 100%;" class=""></div>';
            }
        }



        videoHtml.html(html);
        videoHtml.show();

        videoHtml.attr('data-url','')

        var PlayerFactory = require('player-factory');
        var playerFactory = new PlayerFactory();
        var player = playerFactory.create(
            playerType,
            {
                element: '#lesson-player',
                url: url,
                src:'/static/libs/player/bfplayer/cloud.swf',
                fid:fileId,
                fingerprint: fingerprint,
                fingerprintSrc: fingerprintSrc,
                watermark: watermark,
                starttime: starttime,
                agentInWhiteList: agentInWhiteList,
                timelimit:timelimit,
                token:token
            }
        );

        var messenger = new Messenger({
            name: 'parent',
            project: 'PlayerProject',
            type: 'child'
        });


        player.on("timechange", function(e){
            if(parseInt(player.getCurrentTime()) != parseInt(player.getDuration())){
                DurationStorage.set(userId, fileId, player.getCurrentTime());

                messenger.sendToParent("timechange", {currTime: parseInt(player.getCurrentTime())});
            }
        });

        player.on("firstplay", function(){

        });

        player.on("ready", function(){
            messenger.sendToParent("ready", {pause: true});
            var time = DurationStorage.get(userId, fileId);
            if(time>0){
                player.setCurrentTime(DurationStorage.get(userId, fileId));
            }
            player.play();
        });
        player.on("onMarkerReached",function(markerId,questionId){
            // $('.vjs-break-overlay-text').html("");
            messenger.sendToParent("onMarkerReached", {pause: true,markerId:markerId,questionId:questionId});
        });



        player.on("paused", function(){
            messenger.sendToParent("paused", {pause: true});
        });

        player.on("playing", function(){
            messenger.sendToParent("playing", {pause: false});
        });

        player.on("ended", function(){
            messenger.sendToParent("ended", {stop: true});
            DurationStorage.del(userId, fileId);
        });

    };

    var DurationStorage = {
        set: function(userId,fileId,duration) {
            var durations = Store.get("durations");
            if(!durations || !(durations instanceof Array)){
                durations = new Array();
            }

            var value = userId+"-"+fileId+":"+duration;
            if(durations.length>0 && durations.slice(durations.length-1,durations.length)[0].indexOf(userId+"-"+fileId)>-1){
                durations.splice(durations.length-1, durations.length);
            }
            if(durations.length>=20){
                durations.shift();
            }
            durations.push(value);
            Store.set("durations", durations);
        },
        get: function(userId,fileId) {
            var durationTmpArray = Store.get("durations");
            if(durationTmpArray){
                for(var i = 0; i<durationTmpArray.length; i++){
                    var index = durationTmpArray[i].indexOf(userId+"-"+fileId);
                    if(index>-1){
                        var key = durationTmpArray[i];
                        return parseFloat(key.split(":")[1])-5;
                    }
                }
            }
            return 0;
        },
        del: function(userId,fileId) {
            var key = userId+"-"+fileId;
            var durationTmpArray = Store.get("durations");
            for(var i = 0; i<durationTmpArray.length; i++){
                var index = durationTmpArray[i].indexOf(userId+"-"+fileId);
                if(index>-1){
                    durationTmpArray.splice(i,1);
                }
            }
            Store.set("durations", durationTmpArray);
        }
    };

});