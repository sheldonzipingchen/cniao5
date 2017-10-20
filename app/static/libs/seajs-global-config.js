seajs.config({


    base:'/static/libs/',
    alias: {
        'jquery': 'jquery/1.11.3/jquery.seajs',
        '$': 'jquery/1.11.3/jquery.seajs',
        '$-debug': 'jquery/1.11.3/jquery.seajs',

        'template': 'jquery/jquery-jtemplates-seajs',
        'qrcode': 'jquery/qrcode/jquery.qrcode-seajs',
        'qrcode_base': 'jquery/qrcode/qrcode',
        'paginator': 'jquery/jqPaginator-seajs',
        'jquery.jcrop': 'jquery/jcrop/jquery.Jcrop.min',
        'jquery.jcrop-css': 'jquery/jcrop/jquery.Jcrop.min.css',
        'jquery.zclip': 'jquery/zclip/jquery.zclip.min',
        'jquery-labelauty': 'jquery/jquery-labelauty/jquery-labelauty',
        'jquery-labelauty-css': 'jquery/jquery-labelauty/jquery-labelauty.css',
        'jquery-esn-autobrowse': 'jquery/jquery-esn-autobrowse/jquery.esn.autobrowse.js',
        'jquery-chosen': 'jquery/chosen/chosen.jquery.js',
        'jquery-chosen-css': 'jquery/chosen/chosen.min.css',
        'jquery-fancybox': 'jquery/fancybox/jquery.fancybox',
        'jquery-fancybox-css': 'jquery/fancybox/jquery.fancybox.css',
        'jquery-fullpage': 'jquery/jquery.fullpage/jquery.fullPage.min',
        'jquery-fullpage-css': 'jquery/jquery.fullpage/css/jquery.fullPage.css',

        'webuploader': 'gallery2/webuploader/0.1.2/webuploader',
        'bootstrap': 'gallery2/bootstrap/3.1.1/bootstrap',
         'video-js': 'gallery2/video-js/4.2.1/video-js',

        'bootstrap.validator': 'common/validator',

        'moment': 'gallery/moment/2.5.1/moment',

        'class': 'arale/class/1.1.0/class',
        'base': 'arale/base/1.1.1/base',
        'widget': 'arale/widget/1.1.1/widget',
        'messenger': 'arale/messenger/2.0.0/messenger',

        'position': 'arale/position/1.0.1/position',
        'overlay': 'arale/overlay/1.1.4/overlay',
        'mask': 'arale/overlay/1.1.4/mask',
        'sticky': 'arale/sticky/1.3.1/sticky',
        'cookie': 'arale/cookie/1.0.2/cookie',
        'messenger': 'arale/messenger/2.0.0/messenger',
        "templatable": "arale/templatable/0.9.1/templatable",
        'placeholder': 'arale/placeholder/1.1.0/placeholder',

        'swiper': 'swiper/2.7.6/swiper',
        'echo.js': 'echo/1.7.0/echo',
        'store': 'store/1.3.16/store',


        'ckeditor': 'ckeditor/4.4.8/ckeditor',
        'cniao-ckeditor': 'common/cniao-ckeditor',
        'wang-editor': 'common/wang-editor',
        'cniao.webuploader': 'common/web-uploader',
        'cniao.imagecrop': 'common/image-crop',
        'spin': 'common/spin',
        'message-sender': 'common/message-send',

        'qiniu': 'qiniu/qiniu.min',
        'plupload': 'plupload/plupload.full.min',
        'pace': 'pace/1.0.2/pace.min',
        'pace-css-shop': 'pace/1.0.2/themes/green/pace-theme-flash.css',

        'player-factory': 'player/player-factory',
        'video-player': 'balloon-video-player/1.3.0/index',

        'jquery.perfect-scrollbar': "jquery-plugin/perfect-scrollbar/0.4.8/perfect-scrollbar",
         "jquery.raty": "jquery-plugin/raty/2.5.2/raty",
         "jquery.timeago": "jquery-plugin/timeago/jquery.timeago",
         'jquery-blurr': 'jquery-plugin/jquery.blurr/jquery.blurr',

        'highlight': "ckeditor/4.4.8/plugins/codesnippet/lib/highlight/styles/default.css",
        'highlight.css': "ckeditor/4.4.8/plugins/codesnippet/lib/highlight/highlight.pack",

        'layer': "layer/layer",
        'layer-css': "layer/skin/layer.css"

    },

    // 预加载项
    preload: [this.JSON ? '' : 'json'],

    // 路径配置
    paths: {

        'path-js':'/static/js/',
        'app':'/static/js/app/',
        'admin':'/static/admin/js/',


    },

    // 变量配置
    vars: {
        'locale': 'zh-cn'
    },

    charset: 'utf-8',

    debug: false
});




var version = '1.0.5'
var __SEAJS_FILE_VERSION = '?v' + version;

seajs.on('fetch', function(data) {
    if (!data.uri) {
        return ;
    }

    if (data.uri.indexOf(app.mainScript) > 0) {
        return ;
    }

    data.requestUri = data.uri + __SEAJS_FILE_VERSION;

});

seajs.on('define', function(data) {
    if (data.uri.lastIndexOf(__SEAJS_FILE_VERSION) > 0) {
        data.uri = data.uri.replace(__SEAJS_FILE_VERSION, '');
    }
});