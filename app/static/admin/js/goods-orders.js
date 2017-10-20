
define(function(require, exports, module) {

     require('template');
     require('paginator');
    require("layer")
    require("layer-css")

    var currentPage=1;
    var pageSize=10;
    var totalCount=0;

    var base_url="/admin/goods/orders?"


    initData();





    function initData(){

         $.get(buildUrl(),function(data){




        var pagination = JSON.parse(data);

        totalCount = pagination.totalCount;
        currentPage=pagination.pageIndex;
        //totalPage=data.totalPage;

        $("#data-list").setTemplateURL("/static/jtemplate/admin/goods/orders.html?d="+(+new Date()));

        $("#data-list").processTemplate(pagination.datas);

         initPaginator()



    })
    }

    function initPaginator(){

              $('#pagination').jqPaginator({
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

                                 initData()
                            }

                        }
                    });

            }

    function buildUrl(){


         var url=base_url+ 'page_index='
            +(currentPage)+"&page_size="+pageSize;

        return url


    }


});


