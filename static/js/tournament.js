$(document).ready(function () {
$("id_weight").hide();
    $("#id_type").change(function () {
        var wartosc = $('#id_type').val();
        if (wartosc == "KUMITE") {
            $("id_weight").show();
        }else{
$("id_weight").hide();
}
    });
});