define(function(require, exports, module) {
    var Notify = require('common/bootstrap-notify');

    require('plupload')
   require('qiniu')

    exports.run = function() {


        resizeImg($("#avatar"),200,0);

         var $btn = $("#upload-picture-btn")

        var uploader = Qiniu.uploader({
                runtimes: 'html5,flash,html4',      // 上传模式,依次退化
                browse_button: 'upload-picture-btn',         // 上传选择的点选按钮，**必需**
                uptoken_url : $btn.attr('data-upload-token-url'), // uptoken 是上传凭证，由其他程序生成

                get_new_uptoken: false,             // 设置上传文件的时候是否每次都重新获取新的 uptoken
                save_key:true,
                domain: 'cniao5-imgs.qiniudn.com',     // bucket 域名，下载资源时用到，**必需**
                max_file_size: '2mb',             // 最大文件体积限制
                flash_swf_url: '/static/libs/plupload/Moxie.swf',
                max_retries: 3,                     // 上传失败最大重试次数
                chunk_size: '4mb',                  // 分块上传时，每块的体积
                auto_start: true,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传,
                multi_selection: false,
                filters : {
                    max_file_size : '2mb',
                    prevent_duplicates: true,
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

                        Notify.success('头像上传成功');

                        var domain = "http://"+up.getOption('domain')+"/";
                        var res = Qiniu.parseJSON(info);
                        var sourceLink = domain + res.key;  //获取上传成功后的文件的Url
                         $("#avatar").attr('src',sourceLink)
                        setUserHeadImage($btn.data("save-url"),sourceLink);
                    },
                    'Error': function(up, err, errTip) {

                        Notify.danger('上传失败，请重试！');
                    },
                    'UploadComplete': function() {
                           //队列文件处理完毕后,处理相关的事情
                    },
                    'Key': function(up, file) {

                        var url = $btn.attr('data-file-key-url');
                        $.get(url,function(data){

                            var ext = Qiniu.getFileExtension(file.name);
                            var key = data.result + '.' + ext;
                            return key;
                        })

                    }
                }
            });




    };




    function setUserHeadImage(url,img_url){

        var data={}
        data.logo_url = img_url;

            $.ajax({
                    url:  url,
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                    dataType:'json',
                    type:"POST",
                    success: function(data) {

                        if (data.success) {
//                            Notify.success('修改成功！');

                            window.location.href=$("#upload-picture-btn").data("go-url")

                        } else {
//                            Notify.danger('修改失败！');
                        }
                    },
                    error: function(data) {
                        Notify.danger('系统错误！');
                    }
                });

    }

    var resizeImg=function(objImg,maxWidth,maxHeight){

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

//            objImg.attr('data-natural-width',img.width)
//            objImg.attr('data-natural-height',img.height)

            objImg.attr('width' ,w);
            objImg.attr('height' ,h);
        }


});