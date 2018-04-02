function featureDataInit() {
    $.ajax({
        type: "get",
        dataType: "json",
        url: "/words_data",
        async: true,
        contentType: "application/json",
        success: function (data) {
            // wordsCloud(data);
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

// featureDataInit();