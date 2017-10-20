define(function(require, exports, module) {

    var Spin =require("spin")
    require('template');
    require('paginator');

    require("layer");
    require("layer-css");



     var currentPage=1;
     var pageSize=10;
    var totalCount=0;
    var base_url = "/member/my/orders/list"

    exports.run = function() {

        initThreads();

        $("#orders-table").on('click', '.cancel', function(){



            var this_ =$(this);
            layer.confirm('真的要取消订单吗？', {
                  btn: ['取消','关闭'] //按钮
                }, function(){

                $.post(this_.data('url'), function(data) {
                    if(data.result==false) {
                        layer.msg('订单取消失败！');

                    }
                    else{
                        layer.msg('订单已取消成功！');
                        window.location.reload();
                    }
                });

                }, function(){
                  layer.closeAll()
                });



        });

    };


    function initThreads(){


        var spin = new Spin();

        spin.loading($("#order-list"))



        var url=base_url+"?page_index="+currentPage

        $.get(url,function(data){

            parseData(data);

            spin.stop()

        })
    }



    function parseData(data){

            data  = JSON.parse(data);

            totalCount = data.totalCount;
            // totalPage=data.totalPage;
            currentPage=data.pageIndex;


            var targetEml = $("#order-list");
            if(totalCount<=0){

                var empty = "<div class='empty'>暂无订单</div>"
                targetEml.append(empty);

                return
            }


            targetEml.setTemplateURL("/static/jtemplate/member/orders.html?d=" + (+new Date()));
            targetEml.processTemplate(data.datas);

             initPaginator();
         }

     function initPaginator(){

              $('.pagination').jqPaginator({
                       totalCounts:totalCount,
                       pageSize:pageSize,
                        visiblePages: 5,
                        currentPage: currentPage,
                        prev:'<li><a href="javascript:void(0)"><i class="icon icon-arrow-left3"></i></a></li>',
                        next:'<li><a href="javascript:void(0)"><i class="icon icon-arrow-right3"></i></a></li>',
                        page:'<li><a href="javascript:void(0)">{{page}}</a></li>',
                        onPageChange: function (num, type) {

                            if(type=='change'){

                                currentPage = num;

                                  var url=base_url+'?page_index='+currentPage+"&page_size="+pageSize

                                  $.get(url,function(data){

                                    parseData(data);


                                })
                            }

                        }
                    });

            }


});