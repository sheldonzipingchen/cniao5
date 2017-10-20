


define(function(require, exports, module) {

    window.$ = window.jQuery = require('jquery');

    require('bootstrap');
    require("placeholder");


    require('pace');
    require('pace-css-shop');



    exports.load = function(name) {

        seajs.use(name, function(module) {
            if ($.isFunction(module.run)) {
                module.run();
            }
        });

    };





    var config = $(".js-page-cfg")
    var controllerJS = config.data("controller-js");



    if(controllerJS!='' && controllerJS !=undefined){

        var js = "admin/"+controllerJS
         exports.load(js)
    }




    $("#sideNav").click(function(){
			if($(this).hasClass('closed')){
				$('.navbar-side').animate({left: '0px'});
				$(this).removeClass('closed');
				$('#page-wrapper').animate({'margin-left' : '260px'});

			}
			else{
			    $(this).addClass('closed');
				$('.navbar-side').animate({left: '-260px'});
				$('#page-wrapper').animate({'margin-left' : '0px'});
			}
		});






});


