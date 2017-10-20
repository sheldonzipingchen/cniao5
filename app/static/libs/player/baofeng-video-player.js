define(function(require, exports, module) {

    var Notify = require('common/bootstrap-notify');



    var Widget = require('widget');
    var Store = require('store')
     Class = require('class');


    var BaofengVideoPlayer = Widget.extend({
         _counter: null,

        config : {"width":"100%","height":"100%","id":"cloudsdk","wmode":"transparent"},
        cloudPlayer:null,

    	attrs: {
        	hasPlayerError: false,
            tokenUrl:'',
            token:'',
        	url: '',
            src:'', // 播放器flash 文件的地址
            auto:'0',
            flashvars:'', // Flash 参数
            servicetype:'1',
            uid:'13647602',
            fid:'',
            width:"100%",
            height:"100%",
            starttime: '0',
            timelimit: '10'
        },

        events: {

        },

        setup: function() {


            this._initParam()
            this._initPlayer();
            this.initListener()

			this.set("player", this);

			BaofengVideoPlayer.superclass.setup.call(this);
    	},

        _initParam:function(){

            this.config['src']=this.get('src')
            this.config['width']=this.get('width')
            this.config['height']=this.get('height')

            var flashvars='servicetype='+this.get("servicetype")+"&uid="+this.get("uid")+"&fid="+this.get("fid")+"&auto="+this.get("auto") +"&tk="+this.get("token")

            this.set("flashvars",flashvars)

            this.config['flashvars']=flashvars


        },

        _initPlayer:function(){

            var that = this;
            var elementId = this.element.attr("id");

            var playertpl = '<object width="{width}" height="{height}"  align="middle" id="{id}" type="application/x-shockwave-flash" ' +
                'classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000">' +
                '<param name="movie" value="{src}">' +
                '<param value="always" name="allowscriptaccess">' +
                '<param value="true" name="allowfullscreen">' +
                '<param value="{wmode}" name="wmode" />' +
                '<param value="{flashvars}" name="flashvars" />' +
                '<embed width="{width}" height="{height}" name="{id}" src="{src}" quality="high"  wmode="{wmode}"   flashvars="{flashvars}"  ' +
                'type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" />' +
                '</object>';



            var videoareaname = this.config['id']

            if(typeof(this.config['isautosize'])!='undefined' && this.config['isautosize']==1){


                var pnode = document.getElementById(this.config['id']).parentNode;
                if(pnode.nodeName.toLowerCase() == "body"){
                    pnode.style.overflow = "hidden";
                    pnode.style.margin = "0px auto";
                }
                var swidth = pnode.clientWidth;
                var sheight = pnode.clientHeight;
                pwidth = parseInt(swidth);
                pheight = parseInt(sheight);
                document.getElementById(videoareaname).style.overflow = "hidden";
                document.getElementById(videoareaname).style.margin = "0px auto";
                var pt, pb;
                try{
                    pt = window.getComputedStyle(pnode,null).paddingTop;
                    pb = window.getComputedStyle(pnode,null).paddingBottom;
                }catch(e){
                    pt = pnode.currentStyle.paddingTop;
                    pb = pnode.currentStyle.paddingBottom;
                }
                sheight = sheight - parseInt(pt)- parseInt(pb);
                if(sheight && (typeof sheight == "number") && sheight==sheight && sheight>0){
                }else{
                    sheight = Math.max(swidth / 16 * 9 + 36, sheight);
                    sheight = Math.min(sheight, 900)
                }
                this.config['width']= parseInt(swidth) + "px";
                this.config['height']= parseInt(sheight) + "px";
    //			window.setInterval(cloudsdk.changeSize, 500)
		}
            this.config['wmode'] = 'transparent';
            if( "src" in this.config){
                if(this.config['src'].indexOf("vr=1") != -1){
                    this.config['wmode'] = 'direct';
                }
                that.element.html(this.analyzetpl(playertpl,this.config))
            }

           this.cloudPlayer = this.getSwf()



        },

         _initCounter: function() {

            if (this._counter && this._counter.timerId) {
                clearInterval(this._counter.timerId);
            }

            var self = this;
            this._counter = new Counter(self, this.get('fingerprint'),this.get("fid") );

            this._counter.setTimerId(setInterval(function() {
                self._counter.execute()
            }, 1000));
        },

        getSwf:function(){


            var id = this.config['id']
            var swf,embed,element = document.getElementById(id) || null;
            if (element && element.nodeName.toUpperCase() == 'OBJECT') {
                if (typeof element.SetVariable != 'undefined') {
                    swf = element;
                }else {
                    embed = element.getElementsByTagName('embed')[0];
                    if (embed) {
                        swf = embed;
                    }
                }
            }
            return swf;

        },

        analyzetpl:function(str, data){


          if(data){
            return str.replace(/\{(.*?)\}/ig, function() {
                return data[arguments[1]] || "";
            });
            }
            return str;
        },


        _jsToFlash:function(){

            var swfobject = this.cloudPlayer;
            if(swfobject){

               return swfobject["jsToAction"].apply(swfobject,arguments);

            }

        },

        // flash 回调 JS
        initListener:function(type){

            var that =this;

            window.cloudsdk = {};
            cloudsdk.onActionTojs=function(type,agrgs){


                switch(type){
                    case "cloudstatus":

                        var status = arguments[1];
                        var data = arguments[2];

                        switch (status){

                            case 'START': //播放器初始化
                                console.log(status,data)
                                that._initCounter()
                                break;

                            case 'LOADING': //播放器加载完成
                                console.log(status,data)

                                that.trigger('ready', arguments);
                                break;


                            case 'PLAY': //视频开始播放
                                console.log(status,data)
                                 that.trigger("playing", arguments);
                                break;


                            case 'TIMEING': //视频播放时间

                                data = parseInt(data)
                                that.trigger('timechange', data);

                                break;

                            case 'PAUSE': //视频暂停
                                console.log(status,data)
                                that.trigger("paused", arguments);
                                break;

                            case 'STOP':
                                console.log(status,data)
                                that.trigger('ended', arguments);
                                break;

                            case 'ERROR':
                                that.set("hasPlayerError", true);
                                var message = '您的浏览器不能播放当前视频。';
                                Notify.danger(message, 60);
                                break;

                        }
                        break;
                    case "displayChange":
					    console.log(type + " -- " + arguments[1]) ;
						break;

                    case "playend":
                        console.log(type);
                        break;
                    case "send_barrage_flash":
                        console.log(arguments[1]);
                        break;
                    case "send_barrage_resault":
                        console.log(arguments[1]);
                        break;
                    case "receive_barrage_flash":
                        console.log(arguments[1]);
                        break;
                    case "show_barrage_flash":
                        console.log(arguments[1]);
                        break;
                }

            }


        },

        checkHtml5: function() {
            if (window.applicationCache) {
                return true;
            } else {
                return false;
            }
        },

    	play: function(){

//            this._jsToFlash('play')

            this.cloudPlayer['jsToAction']('play');

    	},

        pause:function(){

             this._jsToFlash('pause')
        },

        seek:function(time){
            this._jsToFlash('seek',time)
        },

        sendMessageToScreent:function(msg){

         this._jsToFlash('sendspemessage',{text:msg,fontsize:14,fontcolor:0xff0000,repeat:1,cycletime:60,randompos:true});
//         this._jsToFlash('send_barrage',{text:msg,usr:'Ivanssss'});
        },

        _onEnded: function(e) {
        	if (this.get("hasPlayerError")) {
		        return ;
		    }
		    var player = this.get("player");

		    player.currentTime(0);
		    player.pause();
        },

         getStatus:function(){



//             {
//            "isFull":true,
//            "totalTime":23.434,
//            "currTime":10.23,
//            "status":"play"  ////四种状态   play    pause   error  stoped
//            }

            var status =  this._jsToFlash('getStatufinfo')
            return JSON.parse(status);
        },

        // 获取当前播放进度
        getCurrentTime: function() {

            var currTime= this.getStatus().currTime
            return parseInt(currTime);
        },

        // 获取总时长
        getDuration: function() {

             var totalTime= this.getStatus().totalTime
            return parseInt(totalTime);
        },

        setCurrentTime: function(time) {
//			this.get("player").currentTime(time);

            this.seek(time)
        },

        isPlaying: function() {
//        	return !this.get("player").paused();

            var status = this.getStatus();
            return status=='play'
        },

        destroy: function() {
//        	this.get("player").dispose();
        }
    });



    var Counter = Class.create({

        initialize: function(player, fingerprint,lesson_id ) {
            this.player = player;
            this.fingerprint = fingerprint;
            this.lessonId = lesson_id
            this.interval =30;
        },

        setTimerId: function(timerId) {
            this.timerId = timerId;
        },

        execute: function() {
            this.messageCounter();
        },

        messageCounter: function() {


            var playCounter = Store.get("lesson_id_" + this.lessonId + "_playCounter");
            if (!playCounter) {
                playCounter = 0;
            }

            playCounter++;


            if (playCounter >= this.interval){

                this.player.sendMessageToScreent(this.fingerprint);
                playCounter=0
            }

            Store.set("lesson_id_" + this.lessonId + "_playCounter", playCounter);
        }


    });



    module.exports = BaofengVideoPlayer;

});