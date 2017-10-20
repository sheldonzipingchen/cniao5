define(function(require, exports, module) {

   require("jquery-blurr");
    exports.run = function() {




        $(".user-center-header").blurr({height:220});

       if($("#thread-list").length>0){

            require("app/thread-list").run()
        }


    };



});