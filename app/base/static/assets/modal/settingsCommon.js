$(document).ready(function() {
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
            $("input[name='ckb']:checked").each(function(i){
                checkids[i] = $(this).val();
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
                    console.log(location.href);
                    window.location.href = "index"
                }
            })
        };
        $("button").addUser()
    });

    // $('#caseCommit0').click(function() {
    //     console.log("submit")
    //     $.fn.caseSubmit = function() {
    //         caseText = $("#caseText0").val()
    //         caseDesc = $("#caseDesc0").val()
    //         caseType = $("#case_type").find("option:selected").index()
    //         console.log(caseType)
    //         var data = {
    //             data: JSON.stringify({
    //                 'text': caseText,
    //                 'desc': caseDesc,
    //                 'type': 1,
    //             }),
    //         };
    //         $.ajax({
    //             type: "POST",
    //             url: "/case_commit",
    //             cache: false,
    //             data:data,
    //             datatype: 'json',
    //             success: function(data){
    //                 console.log(location.href);
    //                 window.location.href = "index"
    //             }
    //         })
    //     };
    //     $("button").caseSubmit()
    // });
    
});
    