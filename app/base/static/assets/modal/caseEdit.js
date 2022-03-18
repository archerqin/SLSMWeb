$(document).ready(function() {
    $("[id^='EditCase'").click(function() {
        editId = $(this).attr("id")
        caseId = editId.substring(8)
        console.log(caseId)
        $.fn.SetCaseInfo = function () {
            var data = {
                data: JSON.stringify({
                    'case_id': caseId,
                })
            };
            $.ajax({
                type: "POST",
                url: "/set_case_info",
                cache: false,
                data: data,
                datatype: 'json',
                success: function (data) {
                    console.log(data)
                    $("#bugCommitModalLabel").text("编辑case"+data.case_id)
                    $("#caseText0").val(data.text)
                    $("#caseDesc0").val(data.detail)

                }
            })
        }
        $("button").SetCaseInfo()
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
})