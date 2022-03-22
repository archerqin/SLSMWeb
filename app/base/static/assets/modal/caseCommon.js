$(document).ready(function() {
    $('#caseCommit').click(function() {
        var case_type = $.cookie('case_type')
        $("#case_type option[value='case"+case_type+"']").attr("selected", true)

        $('#exampleModal').modal('show')
        // success: function (data) {
        //     $("#post").empty()
        //     $.each(data,function(index,item){
        //         var opt=$("<option value="+item.postId+">"+item.postName+"</option>")
        //         $("#post").append(opt)
        //     });
        //     layer.close(index);
        // }
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
            console.log(caseType)
            var data = {
                data: JSON.stringify({
                    'text': caseText,
                    'desc': caseDesc,
                    'type': caseType,
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
                    window.location.href = "index"
                }
            })
        };
        $("button").caseSubmit()
    });
    
});
    