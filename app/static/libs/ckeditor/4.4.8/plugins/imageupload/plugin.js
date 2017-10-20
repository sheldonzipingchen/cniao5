(function() {
    CKEDITOR.plugins.add("imageupload", {
        requires: ["dialog"],
        init: function(a) {
            a.addCommand("imageupload", new CKEDITOR.dialogCommand("imageupload"));
            a.ui.addButton("imageupload", {
                label: "上传图片",//调用dialog时显示的名称
                command: "imageupload",
                icon: this.path + "image.png"//在toolbar中的图标

            });
            CKEDITOR.dialog.add("imageupload", this.path + "dialogs/imageupload.js")

        }

    })

})();