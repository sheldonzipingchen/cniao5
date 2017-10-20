define(function(require, exports, module) {


      var Widget = require('widget');
      require('plupload')
      require('qiniu')

     require('wang-editor/2.1.19/js/wangEditor.js')($);
     require('wang-editor/2.1.19/css/wangEditor.min.css');
     //require('xss.js');




    var Editor =Widget.extend({

        eidtor:null,
        attrs: {
            editor_id:null,
        },

        events: {
        },

        setup: function() {

            this._initEditor();
        },


        _initEditor:function(){

            var eml = this.element

            function  initUpload(){

                    var editor = this;
                    var btnId = editor.customUploadBtnId;
                    var containerId = editor.customUploadContainerId;


                    var tokenUrl =  eml.data("img-upload-token-url");


                    // 创建上传对象

                    var uploader = Qiniu.uploader({
                        runtimes: 'html5,flash,html4',    //上传模式,依次退化
                        browse_button: btnId,       //上传选择的点选按钮，**必需**
                        uptoken_url: tokenUrl,            //Ajax请求upToken的Url，**强烈建议设置**（服务端提供）
                        unique_names: true,
                        domain: 'http://cniao5-imgs.qiniudn.com/',
                            //bucket 域名，下载资源时用到，**必需**
                        //container: containerId,           //上传区域DOM ID，默认是browser_button的父元素，
                        get_new_uptoken: false,  //设置上传文件的时候是否每次都重新获取新的token
                        max_file_size: '2mb',           //最大文件体积限制
                        flash_swf_url: '/static/libs/plupload/Moxie.swf',  //引入flash,相对路径
                        filters: {
                                mime_types: [
                                  //只允许上传图片文件 （注意，extensions中，逗号后面不要加空格）
                                  { title: "图片文件", extensions: "jpg,gif,png,bmp,jpeg" }
                                ]
                        },
                        max_retries: 3,                   //上传失败最大重试次数
                        dragdrop: true,                   //开启可拖曳上传
                        drop_element: containerId,        //拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
                        chunk_size: '4mb',                //分块上传时，每片的体积
                        auto_start: true,                 //选择文件后自动上传，若关闭需要自己绑定事件触发上传
                        init: {
                            'FilesAdded': function(up, files) {

                            },
                            'BeforeUpload': function(up, file) {

                            },
                            'UploadProgress': function(up, file) {
                                // 显示进度条
                                editor.showUploadProgress(file.percent);
                            },
                            'FileUploaded': function(up, file, info) {


                                var domain = up.getOption('domain');
                                var res = $.parseJSON(info);
                                var sourceLink = domain + res.key; //获取上传成功后的文件的Url
                                // 插入图片到editor
                                editor.command(null, 'insertHtml', '<img src="' + sourceLink + '" style="max-width:100%;"/>')
                            },
                            'Error': function(up, err, errTip) {
                                //上传出错时,处理相关的事情
                            },
                            'UploadComplete': function() {

                                // 隐藏进度条
                                editor.hideUploadProgress();
                            }

                        }
                    });


                }
            wangEditor.config.printLog = false;
            var editor = new wangEditor(this.get("editor_id"));


            editor.config.customUpload = true;  // 设置自定义上传的开关
            editor.config.customUploadInit = initUpload;  // 配置自定义上传初始化事件，uploadInit方法在上面定义了


            editor.config.menus = [


            'bold',
            'underline',
            'italic',
            //'strikethrough',
            //'eraser',
            'forecolor',
            //'bgcolor',
            '|',

            'fontfamily',
            'fontsize',
            'head',
            //'unorderlist',
            //'orderlist',
            //'alignleft',
            //'aligncenter',
            //'alignright',
            '|',
            'link',
            'unlink',
            //'table',
            //'emotion',
            'img',
            //'video',
            //'location',

            '|',
            //'undo',
            //'redo',
                 'quote',
             'insertcode',
            'source',
            'fullscreen'
         ];

            // 字号
            editor.config.fontsizes = {
                // 格式：'value': 'title'
                1: '12px',
                2: '14px',
                3: '16px',
                4: '20px',
                5: '22px',
                6: '28px',
                7: '40px'
            };
            // 字体
            editor.config.familys = [
        '宋体',  '微软雅黑',
        'Arial', 'Verdana', 'Georgia','Times New Roman','Trebuchet MS', 'Courier New', 'Impact', 'Comic Sans MS', 'Consolas'
    ];


            editor.create();

            this.eidtor=editor

        },

        getTxt:function (){
         return this.eidtor.$txt
        },

        getText:function (){

            return this.getTxt().text()
        },
        getFormatText:function (){

            return this.getTxt().formatText()
        },

        getHtml:function(){
             //return filterXSS(this.getTxt().html())

            return this.getTxt().html();
        },

        clear:function(){
            this.getTxt().html("<p><br></p>")
        },

        append:function(html){
            this.getTxt().append(html)
        }



    });



    module.exports =Editor




});