define(function(require, exports, module) {

    var Widget = require('widget');
    var chapterAnimate = Widget.extend({
        events: {
            'click .period-list .chapter': 'onClickChapter'
        },

        setup: function() {

        },

        onClickChapter: function(e) {
            var $target = $(e.currentTarget);
            $target.nextUntil(".chapter").animate({
                visibility: 'toggle',
                opacity: 'toggle',
                easing: 'linear'
            });

            var $icon = $target.find(".period-show .icon");
            if ($icon.hasClass('icon-arrow-top')) {
                $icon.removeClass('icon-arrow-top').addClass('icon-arrow-down3');
            } else {
                $icon.removeClass('es-icon-anonymous-iconfont').addClass('icon-arrow-top');
            }

            if($target.data('toggle') && $target.nextUntil(".chapter").height()) {
                $target.data('toggle', false);

            } else {
                $target.data('toggle', true);
            }
        }

    });

    module.exports = chapterAnimate;


});