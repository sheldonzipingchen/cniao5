define(function(require, exports, module) {



    var Validator = require('bootstrap.validator');
    require('common/validator-rules').inject(Validator);
    var Notify = require('common/bootstrap-notify');



    var html = '  <div class="modal" id="send-message-dialog">'

                       +' <div class="modal-dialog">'

                            +'<div class="modal-content clearfix">'

                               +' <div class="modal-header">'
                                +'  <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>'
                                +'  <h4 class="modal-title">发送私信</h4>'
                        +'        </div>'
                        +'        <div class="modal-body">'
                        +'            <div class="text-center"><img class="user-head avatar-md" src="" /></div>'
                        +'            <form id="form-send-message" action="" class="pvl phl " >'
                        +'                <div class="form-group mbs">'
                        +'                   <div class="controls">'
                        +'                      <textarea class="form-control" rows="4" id="txtmsg"></textarea>'
                        +'                   </div>'
                        +'                </div>'

                         +'              <div class="form-group mbs">'
                         +'                <div class="controls">'
                         +'                    <button type="submit" id="send-btn" data-submiting-text="正在发送" class="btn btn-primary  pull-right mts mbl">发送</button>'
                         +'                </div>'
                        +'              </div>'

                         +'           </form>'

                         +'       </div>'
                          +'  </div>'
                       +' </div>'
                        +'</div>'

        if($("#send-message-dialog").length<=0){

             $("body").append(html);
        }


        var $form=$("#form-send-message")

          ///表单验证
        var validator = new Validator({
            element: $form,
            autoSubmit: false,
            onFormValidated: function(error, results) {
                if (error) {
                    return false;
                }


                var data={};
                data.to_user_id=$("#send-message-dialog").data("user-id")
                data.msg=$("#txtmsg").val();

                if(data.to_user_id =='' || data.to_user_id == undefined || data.to_user_id <=0){
                    Notify.warning("接收用户ID为空")
                    return;
                }

                $('#send-btn').button('submit').addClass('disabled');
                $.ajax({
                    url:  "/message/user/message/send",
                    data: JSON.stringify(data),
                    contentType: "application/json; charset=utf-8",
                     dataType:'json',
                    type:"POST",
                    success: function(data) {

                        $('#send-btn').button('reset').removeClass('disabled');
                        if(data.success){

                            $("#send-message-dialog").modal('hide')
                            Notify.success("发送成功");
                            $("#txtmsg").val("")
                        }
                        else{
                            Notify.warning(data.message);

                        }

                    },
                    error: function(data) {
                        Notify.danger('系统错误！');
                        $('#send-btn').button('reset').removeClass('disabled');
                    }
                });

            },
            failSilently: true
        });

        validator.addItem({
            element: "#txtmsg",
            required: true,
            rule: 'minlength{min:5} maxlength{max:200}',
            display: '消息'
        });






    $('body').on('click', '.js-send-message', function() {


        var this_ = $(this);

        var is_login=($("meta[name='is-login']").attr("content")==1?true:false)
        if(!is_login){
            Notify.warning("请先登录,如已登录,请刷新页面")
            return
        }


        var userId = this_.data("user-id");
        var userHead = this_.data("user-head");


        var dialog = $("#send-message-dialog");

        dialog.attr("data-user-id",userId)

        dialog.find(".user-head").attr("src",userHead);


        dialog.modal("show")

    });


});