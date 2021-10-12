$(document).ready(function() {
    $('#caseCommit').click(function() {
        console.log("1111")
        $('#exampleModal').modal('show')
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

                }
            })
        };
        $("button").caseSubmit()
    });
    
});
    