define(function(require, exports, module) {

      var Widget = require('widget');

     require('spin/spin')
     require('spin/jquery.spin')

    var opts = {
            lines: 6, // 花瓣数目
            length: 10, // 花瓣长度
            width: 2, // 花瓣宽度
            radius: 10, // 花瓣距中心半径
            corners: 1, // 花瓣圆滑度 (0-1)
            rotate: 0, // 花瓣旋转角度
            direction: 1, // 花瓣旋转方向 1: 顺时针, -1: 逆时针
            color: '#34a263', // 花瓣颜色
            speed: 1, // 花瓣旋转速度
            trail: 60, // 花瓣旋转时的拖影(百分比)
            shadow: false, // 花瓣是否显示阴影
            hwaccel: false, //spinner 是否启用硬件加速及高速旋转
            className: 'spinner', // spinner css 样式名称
            zIndex: 2e9, // spinner的z轴 (默认是2000000000)
            top: '50%', // spinner 相对父容器Top定位 单位 px
            left: '50%'// spinner 相对父容器Left定位 单位 px
        };



    //
    //var Spin ={
    //
    //
    //    init:function(option){
    //
    //        if(option==undefined)
    //            spinner = new Spinner(opts);
    //        else
    //            spinner = new Spinner(option)
    //
    //    },
    //
    //    spin:function(target){
    //
    //        this.init()
    //
    //        spinner.spin($(target).get(0));
    //
    //    },
    //    stop:function(){
    //        spinner.stop()
    //    }
    //
    //}


    var Spin = Widget.extend({

        spinner:null,
        attrs:{},
        setup:function(){

             this.spinner = new Spinner(opts);
        },

        loading:function(target){


            this.spinner.spin($(target).get(0));

        },
        stop:function(){
            this.spinner.stop()
        }


    })



    module.exports = Spin;
});
