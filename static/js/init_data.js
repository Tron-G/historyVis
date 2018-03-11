function initData() {
    $.ajax({
        type: "get",
        dataType: "json",
        url: "/init",
        async: true,
        contentType: "application/json",
        success: function (data) {

            timeLine(data);
            console.log(data);

        },
        Error: function () {
            console.log("error");
        }
    });

     $(window).resize(function () {
            window.location.reload();
        });
}

initData();