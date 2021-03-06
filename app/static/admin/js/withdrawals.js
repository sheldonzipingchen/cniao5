
define(function(require, exports, module) {

     require('template');
     require('paginator');
    require("layer")
    require("layer-css")

    var currentPage=1;
    var pageSize=10;
    var totalCount=0;

    var base_url="/admin/withdrawals?"


    initData();

    $("#btn-search").on("click",function(){


        initData();

    })


    $("body").on("click",".js-state-update",function(){


        var this_=$(this);

        var url = this_.data("url");
        var message = this_.data("message")


         layer.confirm(message, {
                      btn: ['确定','取消'] //按钮
                    },
                function(){

                         $.post(url,function(data){

                                if (data.success){
                                       window.location.reload()
                                }
                                 else {
                                    layer.msg(data.message)
                                }

                         })

                    },
                function(){

                        layer.closeAll()

                    });




    })




    function initData(){

         $.get(buildUrl(),function(data){




        var pagination = JSON.parse(data);

        totalCount = pagination.totalCount;
        currentPage=pagination.pageIndex;
        //totalPage=data.totalPage;

        $("#data-list").setTemplateURL("/static/jtemplate/admin/withdrawal.html?d="+(+new Date()));

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

        var state=$('input:radio[name=state]:checked').val();;
        var email_or_mobi=$("#email_or_mobi").val()


         var url=base_url+'state='+state + '&email_or_mobi='+email_or_mobi+ '&page_index='
            +(currentPage)+"&page_size="+pageSize;

        return url


    }


});


