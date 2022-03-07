$(document).ready(function() {
    ////setting界面预设信息获取
    $(function(){
        console.log("onload")
        $.ajax({
            type: "POST",
            url: "/get_users",
            cache: false,
            // data:data,
            datatype: 'json',
            success: function(data){
                console.log(data);
            }}
        )
    });

    //// 点击触发加载
    $('#addUser').click(function() {
        console.log("1111")
        $('#addUserModal').modal('show')
        // success: function (data) {
        //     $("#post").empty()
        //     $.each(data,function(index,item){
        //         var opt=$("<option value="+item.postId+">"+item.postName+"</option>")
        //         $("#post").append(opt)
        //     });
        //     layer.close(index);
        // }
    });

    $("#addUserCommit").unbind('click').on('click',function() {
        console.log("2222")
        $.fn.addUser = function() {
            userName = $("#username").val();
            realName = $("#name").val();
            var checkids = [];
            $("input[name='roleCheck']").each(function(i){
                checkids[i] = $(this).prop("checked");
            });
            console.log(userName)
            console.log(realName)
            console.log(checkids)

            var data = {
                data: JSON.stringify({
                    'username':userName,
                    'name':realName,
                    'rolechecks':checkids
                })
            }
            $.ajax({
                type: "POST",
                url: "/add_user",
                cache: false,
                data:data,
                datatype: 'json',
                success: function(data){
                    console.log(data);
                }
            })
        };
        $("button").addUser()
    });
    
});
    