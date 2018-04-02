function getPiesData() {
     $.ajax({
        type: "get",
        dataType: "json",
        url: "/pies_data",
        async: true,
        contentType: "application/json",
        success: function (data) {
             featurePies(data)
        },
        Error: function () {
            console.log("error");
        }
    });


}
function featurePies(data) {
    console.log(data);








}
getPiesData();