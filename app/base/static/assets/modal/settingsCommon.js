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
                var adm = ""
                var ch = ""
                var qd = ""
                var hd = ""
                var cs = ""
                var yy = ""
                var ms = ""
                for (var dCrew in data) {
                    if ($.inArray(2,data[dCrew].uroles) != -1) {
                        adm += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                    }
                    if ($.inArray(4,data[dCrew].uroles) != -1) {
                        ch += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                    }
                    if ($.inArray(5,data[dCrew].uroles) != -1) {
                        qd += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                    }
                    if ($.inArray(6,data[dCrew].uroles) != -1) {
                        hd += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                    }
                    if ($.inArray(7,data[dCrew].uroles) != -1) {
                        cs += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                    }
                    if ($.inArray(8,data[dCrew].uroles) != -1) {
                        yy += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                    }
                    if ($.inArray(9,data[dCrew].uroles) != -1) {
                        ms += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                    }
                };
                hdata = 
                '<tr><td class="table-primary" colspan="3">管理员</td></tr>' + adm +
                '<tr><td class="table-primary" colspan="3">策划</td></tr>' + ch +
                '<tr><td class="table-primary" colspan="3">前端</td></tr>' + qd +
                '<tr><td class="table-primary" colspan="3">后端</td></tr>' + hd +
                '<tr><td class="table-primary" colspan="3">测试</td></tr>' + cs +
                '<tr><td class="table-primary" colspan="3">运营</td></tr>' + yy +
                '<tr><td class="table-primary" colspan="3">美术</td></tr>' + ms
                $('#crews').html(hdata)
                
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
                // checkids[i] = $(this).prop("checked");
                if ($(this).prop("checked")==true) {
                    checkids.push(i)  //因为不是全部显示，需要在后端进行映射
                };
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
                    var adm = ""
                    var ch = ""
                    var qd = ""
                    var hd = ""
                    var cs = ""
                    var yy = ""
                    var ms = ""
                    for (var dCrew in data) {
                        if ($.inArray(2,data[dCrew].uroles) != -1) {
                            adm += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                        }
                        if ($.inArray(4,data[dCrew].uroles) != -1) {
                            ch += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                        }
                        if ($.inArray(5,data[dCrew].uroles) != -1) {
                            qd += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                        }
                        if ($.inArray(6,data[dCrew].uroles) != -1) {
                            hd += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                        }
                        if ($.inArray(7,data[dCrew].uroles) != -1) {
                            cs += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                        }
                        if ($.inArray(8,data[dCrew].uroles) != -1) {
                            yy += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                        }
                        if ($.inArray(9,data[dCrew].uroles) != -1) {
                            ms += "<tr><td>"+data[dCrew].username+"</td><td>"+data[dCrew].name+"</td></tr>"
                        }
                    };
                    hdata = 
                    '<tr><td class="table-primary" colspan="2">管理员</td></tr>' + adm +
                    '<tr><td class="table-primary" colspan="2">策划</td></tr>' + ch +
                    '<tr><td class="table-primary" colspan="2">前端</td></tr>' + qd +
                    '<tr><td class="table-primary" colspan="2">后端</td></tr>' + hd +
                    '<tr><td class="table-primary" colspan="2">测试</td></tr>' + cs +
                    '<tr><td class="table-primary" colspan="2">运营</td></tr>' + yy +
                    '<tr><td class="table-primary" colspan="2">美术</td></tr>' + ms
                    $('#crews').html(hdata)
                    
                }
            });
        }
        $("button").addUser()
    });
    
});
    