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
    })

    $('#case_commit_0').click(function() {
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
    