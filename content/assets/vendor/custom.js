$(document).ready(function () {
    $(".delete-business").click(function () {
        var bid = $(this).attr('data-id');
        var url = "/business/delete/" + bid;
        $(".del-final").attr("href", url);
        $("#deleteModal").modal();
    });

    $(".edit-time").click(function (e) {
        $(".time-form").show();
        $("#time-var").val('1');
        e.preventDefault();
    });

});



