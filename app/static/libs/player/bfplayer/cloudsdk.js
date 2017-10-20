/** 
* @fileOverview 暴风云视频sdk
* @author <a href="http://www.baofengcloud.com/">暴风云</a> 
* @version 0.0.1 
*/ 
(function(exports){
    var cloudsdk = exports.cloudsdk || {},
        parlist = ['servicetype','uid','fid'];
    var swfid,swfobject,onActionlist = {},

        config = {"width":"100%","height":"100%","id":"cloudsdk","wmode":"transparent"};
    var playtpl = '<object width="{width}" height="{height}"  align="middle" id="{id}" type="application/x-shockwave-flash" ' +
                'classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000">' +
                '<param name="movie" value="{src}"><param value="always" name="allowscriptaccess">' +
                '<param value="true" name="allowfullscreen"><param value="{wmode}" name="wmode" />' +
                '<embed width="{width}" height="{height}" name="{id}" src="{src}" quality="high"  wmode="{wmode}" ' +
                'type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" />' +
                '</object>';
    var eventlist = {"ERROR":[],"START":[],"LOADING":[],"PLAY":[],"TIMEING":[],"PAUSE":[],"STOP":[]},
        playconfig = {"vk":"","tk":"","tltime":0,"auto":1,"fmatid":0};
	var pwidth,pheight;
    function getType(obj) {//取得对象的类型
        return Object.prototype.toString.call(obj).match(/^\[object\s(.*)\]$/)[1];
    }
    function analyzetpl(str, data) {
        if(data){
            return str.replace(/\{(.*?)\}/ig, function() {
                return data[arguments[1]] || "";
            });
        }
        return str;
    }
    function getSwf(id){
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
    }
    function verification(par,json){
        var bool = true;
        for(var i=0,l=par.length;i<l;i++){
            if(!(par[i] in json)){
                bool = false;
                break;
            }
        }
        return bool;
    }
    function assembled(name,par,json){
        var key,vks = [];
        for(var i=0,l=par.length;i<l;i++){
            key = par[i];
            vks.push(key,'=',json[key],'&');
            delete json[key];
        }
        vks[vks.length-1] = ",";
        json[name] = vks.join().replace(/\,/g,'');
        return json;
    }
    function cloudstatus(){
        var arg = Array.prototype.slice.call(arguments);
        var list,fun,key = arg.shift(); 
        if(key in eventlist){
            list = eventlist[key];
            for(var i=0,l=list.length;i<l;i++){
                fun = list[i];
                fun.apply(fun,arg);
            }
        }           
    }
    function onJsToaction(){
        swfobject || (swfobject = getSwf(swfid));
        if(swfobject){
            return swfobject["jsToAction"].apply(swfobject,arguments);
        }       
    }


    /** 
    * @description 初始化创建云播放器 
    * @param {string} id 播放器插入对象id 
    * @param {json} json 启播json串
    */     
    cloudsdk.initplay = function(id,json){
        var playContainer = document.getElementById(id);
        for(var key in json){
            config[key] = json[key];
        }
        swfid = config["id"];
		if(typeof(config['isautosize'])!='undefined' && config['isautosize']==1){
			
			var pnode = document.getElementById(videoareaname).parentNode;
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
			config['width']= parseInt(swidth) + "px";
			config['height']= parseInt(sheight) + "px";
			window.setInterval(cloudsdk.changeSize, 500)
		}
		config['wmode'] = 'transparent';
        if(playContainer && "src" in config){
        	if(config['src'].indexOf("vr=1") != -1){
        		config['wmode'] = 'direct';
        	}
            playContainer.innerHTML = analyzetpl(playtpl,config);
        }
        onActionlist['cloudstatus'] =  cloudstatus;
				videoareaname = config['id'];
    }
	cloudsdk.changeSize = function(){
		var pnode = document.getElementById(videoareaname).parentNode;
		var swidth = pnode.clientWidth;
		var sheight = pnode.clientHeight;
		if(swidth == pwidth && sheight == pheight)return;
		document.getElementById(videoareaname).style.width = swidth + "px";
		document.getElementById(videoareaname).style.height = sheight + "px";
		swfobject || (swfobject = getSwf(swfid));
        if(swfobject){
            swfobject.width = swidth + "px";
			swfobject.height = sheight + "px";
        }
	}
	
    cloudsdk.nextplay = function(json){
        if(verification(parlist,json)){
            json = assembled("vk",parlist,json);
        }
        if("vk" in json){
            for(var key in json){
                playconfig[key] = json[key];
            }       
            onJsToaction('changevideo',playconfig.vk,playconfig.tk,playconfig.auto,playconfig.tltime,playconfig.fmatid);           
        }        
    }
    cloudsdk.addeventlistener = function(key,fun){
        if(key in eventlist){
            eventlist[key].push(fun);
        }
    }     
    cloudsdk.onActionTojs = function(){
        var arg = Array.prototype.slice.call(arguments);
        var type = arg.shift(),data = true,fun;
        if(type in onActionlist){
            fun = onActionlist[type];
            if(getType(fun) == "Array"){
                return fun[1].apply(fun[0],arg);
            }else{
                return fun.apply(this,arg);
            }
        }
        return data;        
    }       
    exports.cloudsdk = cloudsdk;
}(typeof exports === "object" ? exports : window));
