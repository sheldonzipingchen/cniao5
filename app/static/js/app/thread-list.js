define(function(require, exports, module) {


    var Spin =require("spin")
    require('template');
    require('jquery.timeago');


    var currentPage=1;
    var pageSize=10;
    var totalCount=0;
    var totalPage=0;
    var targetId =0;
    var targetType ='';
    var order_by=0;
    var is_hot=0;
    var base_url ="/api/v1/thread/pagination?"

    var threadParamsEml;

    exports.run = function() {




        threadParamsEml =$(".js-thread-query-params");
        targetId = threadParamsEml.data("target-id")
        targetType = threadParamsEml.data("target-type")

        initThreads()

        $(".js-load-more").on('click',function(){


            var this_=$(this)

            this_.text("正在加载....").toggleClass('disabled')

            currentPage+=1;


            if(currentPage>totalPage){
                currentPage=1
            }
            var url=base_url+'target_id='+targetId + '&target_type='+targetType+ '&page_index='
            +(currentPage)+"&page_size="+pageSize+"&order_by="+order_by +"&is_hot="+is_hot

            $.get(url,function(data){


                    totalCount = data.totalCount;
                    currentPage=data.pageIndex;
                    totalPage=data.totalPage;

                        var template = $.createTemplateURL('/static/jtemplate/forum/threads.html')

                       //data.is_admin=threadParamsEml.data("is-admin");
                        //data.forum_id=targetId


                        var params={}
                        params["is_admin"]=threadParamsEml.data("is-admin")
                        params["forum_id"]=targetId

                        var html= $.processTemplateToText(template,data.datas,JSON.stringify(params))


                      $("#thread-list").append(html)
                       this_.text("浏览更多").toggleClass('disabled')
                      $(".timeago").timeago();
                  })

        })


        $(".js-thread-sort").on('click', function () {


            var $this = $(this);

            $(".js-current-thread-sort").html($this.children("a").text())

            threadParamsEml.data("order-by",$this.data("order-by"))

            currentPage=1
            initThreads();

        })


        $(".js-thread-type").on('click',function(){

            var $this = $(this);
            $(".js-thread-type").removeClass("active");
            $this.addClass('active');

             initThreads();

        })


        $("body").on('click','.js-hot-setting',function(){

            var this_=$(this)

            $.post(this_.data("url"),function(data){

                if(data.success){
                    this_.text("取消热门")
                }

            })

        })

    };


    function initThreads(){


        var spin = new Spin();

        spin.loading($("#thread-list"))

         order_by = threadParamsEml.data("order-by");
        if (order_by==undefined || order_by=='')
            order_by=0;

         is_hot = $(".js-thread-type.active").data("is-hot");
        if (is_hot==undefined || is_hot=='')
            is_hot=0;

        var url=base_url+'target_id='+targetId + '&target_type='+targetType+ '&page_index='
            +currentPage+"&page_size="+pageSize+"&order_by="+order_by +"&is_hot="+is_hot

        $.get(url,function(data){

            parseData(data);

            spin.stop()

        })
    }



    function parseData(data){

            totalCount = data.totalCount;
            totalPage=data.totalPage;
            currentPage=data.pageIndex;

            if(totalCount<=0){

                var empty = "<div class='empty'>暂无数据</div>"
                 $("#thread-list").append(empty);

                return
            }
            if (data.datas.length==0){
                          currentPage=1
            }
            $(".js-load-more").removeClass("hidden")

            if(targetType=='course') {
                $("#thread-list").setTemplateURL("/static/jtemplate/course/course_threads.html?d=" + (+new Date()));
                $("#thread-list").processTemplate(data.datas);
            }
            else if (targetType=='forum'){


                $("#thread-list").setTemplateURL("/static/jtemplate/forum/threads.html?d="+(+new Date()));

                $("#thread-list").setParam("is_admin",threadParamsEml.data("is-admin"));
                $("#thread-list").setParam("forum_id",targetId);

                $("#thread-list").processTemplate(data.datas);
            }
            else if (targetType=='user'){
                $("#thread-list").setTemplateURL("/static/jtemplate/user/blogs.html?d="+(+new Date()));
                $("#thread-list").processTemplate(data.datas);
            }



            $(".timeago").timeago();
             //initPaginator();
         }





});