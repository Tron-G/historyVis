function mainview() {
    $.ajax({
        type: "get",
        dataType: "json",
        url: "/init",
        async: true,
        contentType: "application/json",
        success: function (data) {

            var w = 1000;
            var h = 600;
            var svg = d3.select("#main")
                .append("svg")
                .attr("width", w)
                .attr("height", h);

            svg.append("rect")
                .attr("x", 50)
                .attr("y", 50)
                .attr("width", 30)
                .attr("height", 10)
                .attr("fill", "steelblue");

            svg.selectAll("text")
                .data(data)
                .enter()
                .append("text")
                .attr("x", function (d, i) {
                    return i*40;
                })
                .attr("y", 100)
                .attr("fill", "green")
                .attr("font-size", 30)
                .attr("font-family", "simsun")
                .text(function (d) {
                    return d.id;
                });


            console.log(data);

        },
        Error: function () {
            console.log("error");
        }
    });

}

mainview();