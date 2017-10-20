

define(function(require, exports, module) {

    var Widget = require('widget');

    var Foot_AD = Widget.extend({



        attrs: {
            goUrl: null,
            adImgUrl: null,

        },


        setup: function() {



            var html='<div class="float_mask hidden-xs" id="float_mask">'
                +'<div class="float_layer">'
                +'</div>'
                +'<div class="float_content clearfix">'
                +'  <div class="float_bg">'
                +'        <a target="_blank" href="'+this.get("goUrl")+'" title="">'
                +'            <div class="float_slogan">'
                +'                 <img src="'+this.get('adImgUrl')+'" alt="">'
                +'            </div>'
                +'        </a>'
                 +'   </div>'
                +'</div>'
               +' <div class="float_close">'
                +'    <a href="javascript:void(0)">'
                 +'       <img src="/static/images/close.png" alt="">'
                  +'  </a>'
                +'</div>'
            +'</div>';


            $(html).appendTo($("body"))

            $(".float_close").on('click',function(){

                $(".float_mask").addClass("hidden")
            })


        },


        show: function() {

        },

        hide: function() {

        }



    });

    module.exports = Foot_AD;

});
