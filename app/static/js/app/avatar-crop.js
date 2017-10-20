define(function(require, exports, module) {
    var Notify = require('common/bootstrap-notify');
    var ImageCrop = require('cniao.imagecrop');

    exports.run = function() {




        var imageCrop = new ImageCrop({
            element: "#avatar-crop",
            cropedWidth: 200,
            cropedHeight: 200,
            maxWidth:300,
            maxHeight:300
        });


        imageCrop.on("afterCrop", function(response){


            if(response.success){
                Notify.success('保存成功');
                 document.location.href=$("#upload-avatar-btn").data("gotoUrl");
            }


        });

        $("#upload-avatar-btn").click(function(e){
            e.stopPropagation();

            imageCrop.crop()

        })

        $('.go-back').click(function(){
            history.go(-1);
        });
    };

});