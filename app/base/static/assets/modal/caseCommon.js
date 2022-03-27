$(document).ready(function() {
    $('#caseCommit').click(function() {
        var case_type = $.cookie('case_type')
        $("#case_type option[value='case"+case_type+"']").attr("selected", true)
        $.ajax({
            type: "POST",
            url: "/get_versions",
            cache: false,
            // data:data,
            datatype: 'json',
            success: function (data) {
                $("#select_ver").empty()
                $.each(data.slice(0,3),function(index,item){
                    var opt=$("<option value="+item.verid+">"+item.vername+"</option>")
                    $("#select_ver").append(opt)
                });
            // layer.close(index);
            }
        });
        $('#exampleModal').modal('show')
    });

    $("[id^='confirmCaseDelete'").unbind('click').on('click',function() {
        console.log("2222")
        $.fn.caseDelete = function() {
            var case_id = $(event.target).attr("id").substring(17)
            console.log(case_id)
            var data = {
                data: JSON.stringify({
                    'id':case_id
                })
            }
            $.ajax({
                type: "POST",
                url: "/case_delete",
                cache: false,
                data:data,
                datatype: 'json',
                success: function(data){
                    console.log(location.href);
                    window.location.href = "index"
                }
            })
        };
        $("button").caseDelete()
    });

    $('#caseCommit0').click(function() {
        console.log("submit")
        $.fn.caseSubmit = function() {
            caseText = $("#caseText0").val()
            caseDesc = $("#caseDesc0").val()
            caseType = $("#case_type").find("option:selected").index() + 1
            caseVer = $("#select_ver").val()
            var data = {
                data: JSON.stringify({
                    'text': caseText,
                    'desc': caseDesc,
                    'type': caseType,
                    'ver':caseVer,
                }),
            };
            $.ajax({
                type: "POST",
                url: "/case_commit",
                cache: false,
                data:data,
                datatype: 'json',
                success: function(data){
                    console.log(location.href);
                    window.location.href = "case_online"
                }
            })
        };
        $("button").caseSubmit()
    });
    
});
    