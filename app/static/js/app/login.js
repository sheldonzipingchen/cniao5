define(function(require, exports, module) {


    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);
    require("placeholder");


    //require("cookie")

    exports.run = function() {





        var validator = new Validator({
            element: '#login-form'
        });
        validator.addItem({
            element: '[name="email"]',
            required: true,
            display:"手机/邮箱"
        });
        validator.addItem({
            element: '[name="password"]',
            required: true,
            display:"密码"
        });







    };

});