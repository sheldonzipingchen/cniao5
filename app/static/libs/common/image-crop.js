define(function(require, exports, module) {
    var Notify = require('common/bootstrap-notify');
    var Widget = require('widget');
//     require('qiniu')
    require("jquery.jcrop-css");
    require("jquery.jcrop");

    var ImageCrop = Widget.extend({


        events: {

        },

    	setup: function(){
	    	var self = this;
	    	var $picture = this.element;



            self.resizeImg($picture,300,0)



	        var scaledWidth = $picture.attr('width'),
	            scaledHeight = $picture.attr('height'),
	            naturalWidth = $picture.data('naturalWidth'),
	            naturalHeight = $picture.data('naturalHeight'),
	            cropedWidth = this.get("cropedWidth"),
	            cropedHeight = this.get("cropedHeight"),
	            ratio = cropedWidth / cropedHeight,

	            selectWidth = (cropedWidth) * (naturalWidth/scaledWidth),
	            selectHeight = (cropedHeight) * (naturalHeight/scaledHeight),

                maxWidth = this.get("maxWidth"),
                maxHeight = this.get("maxHeight");

	        var img = $.Jcrop($picture, {
//	            trueSize: [naturalWidth, naturalHeight],
                maxSize:[maxWidth,maxHeight] ,
                minSize:[cropedWidth,cropedHeight],
	            setSelect: [0, 0, selectWidth, selectHeight],
	            aspectRatio: ratio,
	            onSelect: function(c) {
	                self.trigger("select", c);
	            }
	        });
	        self.set("img", img);
        },

        crop: function(postData){
            var self = this;

        	if(!postData) {
        		postData = {};
        	}


        	postData = $.extend(this.get("img").tellScaled(),

                postData, {width: this.element.width(),
                height: this.element.height()});


            var img_url = self.element.attr("src")
            img_url = img_url+"?imageMogr2/thumbnail/"+postData.width+"x"+postData.height+"/crop/!"+postData.w+"x"+postData.h+"a"+postData.x+"a"+postData.y;

            var data={}
            data.logo_url = img_url;
            $.ajax({
                    url:  self.element.data('url'),
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                      self.trigger("afterCrop", data);
                    },
                    error: function(data) {
                        Notify.danger('系统错误！');
                    }
                });

        },

        resizeImg:function(objImg,maxWidth,maxHeight){

            var img = new Image();
            img.src = objImg.attr("src");

            var hRatio;
            var wRatio;
            var Ratio = 1;

            var w = img.width;
            var h = img.height;

            if(w ==0){

                $.ajax({
                  type : "get",
                  url : img.src+"?imageInfo",
                  async : false,
                  success : function(data){

                      w=data.width
                      h=data.height
                  }
                });
            }


             console.log(w)
             console.log(h)

            wRatio = maxWidth / w;
            hRatio = maxHeight / h;
            if (maxWidth ==0 && maxHeight==0){
            Ratio = 1;
            }else if (maxWidth==0){//
            if (hRatio<1) Ratio = hRatio;
            }else if (maxHeight==0){
            if (wRatio<1) Ratio = wRatio;
            }else if (wRatio<1 || hRatio<1){
            Ratio = (wRatio<=hRatio?wRatio:hRatio);
            }
            if (Ratio<1){
            w = w * Ratio;
            h = h * Ratio;
            }

            objImg.attr('data-natural-width',img.width)
            objImg.attr('data-natural-height',img.height)

            objImg.attr('width' ,w);
            objImg.attr('height' ,h);
        }

    });

	module.exports = ImageCrop;
});