$(document).ready(function () {
    $("#checked").click(function () {
        var input_string = $("#forminput").val();
        $.ajax({
            url: "/ajaxexample_json",
            type: "POST",
            dataType: "json",
            data: {
                client_response: input_string,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function (json) {
                $('#result').append('Server Response: ' + json.server_response);
            },
            error: function (xhr, errmsg, err) {
                alert(xhr.status + ": " + xhr.responseText);
            }
        });
        return false;
    });
});
