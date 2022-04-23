$(document).ready(function() {
    ////setting界面预设信息获取                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    $(function(){
        $.ajax({
            type: "POST",
            url: "/get_users",
            cache: false,
            // data:data,
            datatype: 'json',
            success: function(data){
                set_userlist(data)
            }
        })
    });
    // 加载版本信息
    $(function(){
        $.ajax({
            type: "POST",
            url: "/get_versions",
            cache: false,
            // data:data,
            datatype: 'json',
            success: function(data){
                set_verlist(data)
            }

        });
    });
    // 加载项目信息
    $(function(){
        // console.log("setproj")
        $.ajax({
            type: "POST",
            url: "/get_projects",
            cache: false,
            // data:data,
            datatype: 'json',
            success: function(data){
                set_projlist(data)
            }

        });
    });
    // 重置角色User列表信息
    function set_userlist(data){
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
    // verlist全局变量
    var verList=[];
    // 重置版本verison列表信息
    function set_verlist(data){
        var verlist = ""
        if (data.length !== 0){
            for (var ver in data) {
                verlist += "<tr><td>"+data[ver].verlg+"</td><td><a href='#'><div "+"id='verID2Desc"+data[ver].verid+"'>" 
                +data[ver].vername+"</div></a></td><td>"+data[ver].timestamp+"</td></tr>"
            }
            $('#verlist').html(verlist)
            // console.log(data[0].verdesc)
            $('#onVerDesc').val(data[0].vername+"版本信息\n"+data[0].verdesc)
        }
    }

    // 项目信息加载
    function set_projlist(data){
        var projlist = ""
        if (data.length !== 0){
            for (var proj in data) {
                projlist += "<tr><td>"+data[proj].projname+"</td><td>"
                +data[proj].langname+"</td><td>"
                +data[proj].projalias+"-"+data[proj].langalias+"</td><td>"
                +"<a id=projEdit"+data[proj].projid+" href='#'>编辑</a>" + "&ensp;"
                +"<a id=projDel"+data[proj].projid+" href='#'>删除</a>" 
                +"</td></tr>"
            }
            console.log(projlist)
            $('#projlist').html(projlist)
        }
    }

    //// 点击触发加载
    $('#addUser').click(function() {
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
                    set_userlist(data)
                }
            });
        }
        $("button").addUser()
    });

    // 打开版本号增加modal
    $('[id^=addver]').click(function() {
        // Swal.fire("hahahaha")
        typeID = $(this).attr("id").substring(7)
        $.ajax({
            type: "POST",
            url: "/gen_version/"+typeID,
            cache: false,
            // data:data,
            datatype: 'json',
            success: function(data){
                $("#version_name").val(data)
            }

        });
        $('#addVerModal').modal('show')

    });

    // 提交新版本号
    $('#addVerCommit').click(function() {
        version_name = $("#version_name").val()
        version_desc = $("#version_desc").val()
        var data = {
            data: JSON.stringify({
                'vername':version_name,
                'verdesc':version_desc,
            })
        };
        $.ajax({    
            type: "POST",
            url: "/add_version",
            cache: false,
            data:data,
            datatype: 'json',
            success: function(data){
                set_verlist(data)
            }
        })
    });
    // 提交新项目（语言）
    $('[id^=addProjCommit').click(function() {
        proj_name = $("#proj_name").val()
        proj_alias = $("#proj_alias").val()
        lang_name = $("#lang_name").val()
        lang_alias = $("#lang_alias").val()
        var data = {
            data: JSON.stringify({
                'projname':proj_name,
                'projalias':proj_alias,
                'langname':lang_name,
                'langalias':lang_alias,
            })
        };
        $.ajax({    
            type: "POST",
            url: "/add_project/"+"0",
            cache: false,
            data:data,
            datatype: 'json',
            success: function(data){
                set_projlist(data)
            }
        })
    });


    //根据versionname上的id显示具体desc
    $('body').on("click", '[id^=verID2Desc]',function() {
        verID = $(this).attr("id").substring(10)
        $.ajax({
            type: "POST",
            url: "/get_verdesc/"+verID,
            cache: false,
            // data:data,
            datatype: 'json',
            success: function(data){
                $("#onVerDesc").val(data["vername"]+"版本信息\n"+data["verdesc"])
            }

        });
    });

    //// 打开增加项目modal
    $('#addProj').click(function() {
        $('#addProjModal').modal('show')
    });

    //// 打开编辑项目modal
    $('body').on("click", '[id^=projEdit]',function() {
        projId = $(this).attr("id").substring(8)
        console.log(projId)

        $('#addProjModal').modal('show')
    });
    //// 删除项目model
    $('body').on("click", '[id^=projDel]',function() {
        projId = $(this).attr("id").substring(7)
        console.log(projId)

        $('#addProjModal').modal('show')
    });
    

    
});
    