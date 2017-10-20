define(function(require, exports, module) {




    require("layer")
    require("layer-css")




    exports.run = function() {



          $(".empty-section").on('click',function () {


              openWindow("/member/invite/cash","a__","_blank")

          })





    };



    function openWindow(url, emlId,openType) {
                  var a = document.createElement('a');
                  a.setAttribute('href', url);
                  a.setAttribute('target',openType);
                  a.setAttribute('id', emlId);
                  a.setAttribute('style','display:none')

                var span = "<span id ='"+emlId+"_span'>click</span>"
                a.innerHTML =span;

                  // 防止反复添加

              var aEml = document.getElementById(emlId)
              if(!aEml) {
                  document.body.appendChild(a);
              }else{
                  aEml.setAttribute('href', url);
              }

             $("#"+emlId+"_span").trigger('click');

            return false;
        }






});