(function() {
    CKEDITOR.dialog.add("imageupload",
        function(editor) {
            return {
                title: "上传图片",
                minWidth: "600px",
                minHeight:"300px",
                contents: [{
                    id: "tab1",
                    label: "",
                    title: "",
                    expand: true,
                    width: "420px",
                    height: "300px",
                    padding: 0,
                    elements: [{
                        type: "html",
                        style: "width:600px;height:300px",
                        html: '<iframe id="uploadFrame" src="/common/tool/image/upload" frameborder="0"></iframe>'
                    }]
                }],
                onOk: function() {


                    var e = editor;
                    var uploadFrame = document.getElementById("uploadFrame").contentWindow

                    var ul = uploadFrame.document.getElementById("ul_pics");

                    var childs = ul.childNodes
                    for(var i = childs.length - 1; i >= 0; i--) {
                        var node = childs[i];
                        if(node.nodeName == 'LI' || node.nodeName=='li') {

                            var className = node.getAttribute("class");
                            if(className=='img active'){

                                var imageEml =node.firstChild;
                                var url =imageEml.getAttribute("src");

                                var img = editor.document.createElement( 'img', {
                                    attributes: {
                                        src: url,

                                    }
                                } );

                                editor.insertElement( img );

                            }

                        }

                    }
                },
                onShow: function () {

                    //document.getElementById("uploadFrame").setAttribute("src","/common/tool/image/upload?v=' +new Date().getSeconds() + '");
                },


            }
        })
}


)();