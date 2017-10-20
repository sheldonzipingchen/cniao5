/**
 * Created by Ivan on 15/4/20.
 */

$(function(){


    $("#addChapter").click(function(){


       $(this).hide();

        $(".add-chapter-editor").removeClass("hide");
        $(".add-chapter-editor").show();


    });

    $("#btnCancleAddChapter").click(function(){

        $(this).parent().parent().hide();
        $("#addChapter").show();

    });


    $("#addLesson").click(function(){

        $(this).hide();

        $(".add-item-editor").removeClass("hide");
        $(".add-item-editor").show();


    });

    $("#btnCancleAddItem").click(function(){

        $(".add-item-editor").hide();
        $("#addLesson").show();

    });





//    讲师上传头像


    var btnSelectPic =  $("#btnSelectPic");

    btnSelectPic.cropperUpload({
        url: "",
        fileSuffixs: ["jpg", "png", "bmp"],
        errorText: "{0}",
        onComplete: function (msg) {
            console.log("msg"+msg);
            $("#imgPreview").attr("src", msg);
        },
        cropperParam: {//Jcrop参数设置，除onChange和onSelect不要使用，其他属性都可用
            maxSize: [180, 180],//不要小于50，如maxSize:[40,24]
            minSize: [50, 50],//不要小于50，如minSize:[40,24]
            bgColor: "black",
            bgOpacity: .4,
            allowResize: true,
            allowSelect: false,
            animationDelay:50
        },
        perviewImageElementId: "divPreview", //设置预览图片的元素id
        perviewImgStyle: { width: '300px', height: '300px', border: '1px solid #ebebeb' }//设置预览图片的样式
    });



    var imgs = btnSelectPic.data("uploadFileData");



        $("#btnUpload").click(function () {

            console.log("aaaaaaa")
            imgs.submitUpload();
        });

})