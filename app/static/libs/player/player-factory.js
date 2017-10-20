define(function(require, exports, module) {

    var Widget = require('widget');


    var PlayerFactory = Widget.extend({
        attrs: {
        },

        events: {
        },

        setup: function() {
        },

        create: function(type, options){

            switch(type){
                case "normal-video":
                    var NormalVideoPlayer = require('./normal-video-player');
                    return new NormalVideoPlayer(options);
                    break;
                case "baofeng-video":
                    var BaofengVideoPlayer = require('./baofeng-video-player');
                    return new BaofengVideoPlayer(options);
                    break;

            }

        },

        destroy: function(){
        }
    });

    module.exports = PlayerFactory;

});