$(document).ready(function() {
    $('#caseCommit').click(function() {
        console.log("1111")
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

    $("[id^='confirmCasDelete'").unbind('click').on('click',function() {
        console.log("2222")
        $.fn.caseDelete = function() {
            
            var button_val = $(this).html()
            console.log(button_val)
            var case_id = $(this).attr("id").substring(10)
            console.log(case_id)
            // $.ajax({
            //     type: "POST",
            //     url: "/case_delete",
            //     cache: false,
            //     data:data,
            //     datatype: 'json',
            //     success: function(data){
            //         console.log(location.href);
            //         window.location.href = "index"
            //     }
            // })
        };
        $("button").caseDelete()
    });

    $('#caseCommit0').click(function() {
        console.log("submit")
        $.fn.caseSubmit = function() {
            caseText = $("#caseText0").val()
            caseDesc = $("#caseDesc0").val()
            var data = {
                data: JSON.stringify({
                    'text': caseText,
                    'desc': caseDesc,
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
    