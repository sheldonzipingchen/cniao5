define(function(require, exports, module) {
    var Notify = require('common/bootstrap-notify');
    var Widget = require('widget');
//    require('webuploader');
    require('plupload')
    require('qiniu')

    var Uploader = Widget.extend({
        attrs: {
            fileSizeLimit: 2*1024*1024,
            type: '',
            fileInput: '',
            title: '上传',
            formData: {},
            accept: {
	            title: 'Images',
	            extensions: 'gif,jpg,jpeg,png,ico',
	            mimeTypes: 'image/*'
	        },
	        uploader: null,
	        fileVal: 'file'
        },

        events: {
            'click' : "onClick"
        },

        setup: function() {
        	var self = this;
//        	var path = require.resolve("webuploader").match(/[^?#]*\//)[0];
//        	var formData = $.extend(self.get("formData"), {token: self.element.data("uploadToken")});
//		    var uploader = WebUploader.create({
//		        swf: path + "Uploader.swf",
//		        server: app.uploadUrl,
//		        pick: {
//		        	id: '#'+self.element.attr("id"),
//		        	multiple:false
//		        },
//		        formData: $.extend(formData, {'_csrf_token': $('meta[name=csrf-token]').attr('content') }),
//		        accept: self.get("accept"),
//				auto: true,
//				fileNumLimit: 1,
//				fileSizeLimit: self.get("fileSizeLimit")
//		    });



            var uploader = Qiniu.uploader({
                runtimes: 'html5,flash,html4',      // 上传模式,依次退化
                browse_button: self.element.attr("id"),         // 上传选择的点选按钮，**必需**
                uptoken_url : self.element.attr('data-upload-token-url'), // uptoken 是上传凭证，由其他程序生成

                get_new_uptoken: false,             // 设置上传文件的时候是否每次都重新获取新的 uptoken
                domain: 'cniao5-imgs.qiniudn.com',     // bucket 域名，下载资源时用到，**必需**
//                container: 'container',             // 上传区域 DOM ID，默认是 browser_button 的父元素，
                max_file_size: '2mb',             // 最大文件体积限制
                flash_swf_url: '/static/libs/plupload/Moxie.swf',
                max_retries: 3,                     // 上传失败最大重试次数
                chunk_size: '4mb',                  // 分块上传时，每块的体积
                auto_start: true,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传,
                multi_selection: false,
                filters : {
                    max_file_size : '2mb',
                    prevent_duplicates: true,
                    // Specify what files to browse for
                    mime_types: [
                        {title : "Image files", extensions : "jpg,gif,png"} // 限定jpg,gif,png后缀上传
                    ]
                },

                init: {
                    'FilesAdded': function(up, files) {
                        plupload.each(files, function(file) {
                            // 文件添加进队列后,处理相关的事情
                        });
                    },
                    'BeforeUpload': function(up, file) {
                           // 每个文件上传前,处理相关的事情
                    },
                    'UploadProgress': function(up, file) {
                           // 每个文件上传时,处理相关的事情
                    },
                    'FileUploaded': function(up, file, info) {

                    },
                    'Error': function(up, err, errTip) {
                           //上传出错时,处理相关的事情
                    },
                    'UploadComplete': function() {
                           //队列文件处理完毕后,处理相关的事情
                    },
                    'Key': function(up, file) {


                        var url = self.element.attr('data-file-key-url');
                        $.get(url,function(data){

                            return data.result;
                        })

                    }
                }
            });




//		    uploader.on( 'fileQueued', function( file ) {
//
//		    });
//
//		    uploader.on( 'uploadSuccess', function( file, response ) {
//		        self.trigger("uploadSuccess", file, response);
//		    });
//
//		    uploader.on( 'uploadError', function( file, response ) {
//		        Notify.danger('上传失败，请重试！');
//		    });
//
//		    uploader.on('error', function(type){
//		    	switch(type) {
//			    	case "Q_EXCEED_SIZE_LIMIT":
//			    		Notify.danger('文件过大，请上传较小的文件！');
//			    		break;
//		    		case "Q_EXCEED_NUM_LIMIT":
//		    			Notify.danger('添加的文件数量过多！');
//			    		break;
//			    	case "Q_TYPE_DENIED":
//		    			Notify.danger('文件类型错误！');
//			    		break;
//		    	}
//		    });

		    this.set("uploader", uploader);
		},

		onClick: function(){
//			this.get("uploader").upload();
            console.log("onClick -------")
		},

		enable: function(){
		    this.get("uploader").enable();
		}

    });

	module.exports = Uploader;

});