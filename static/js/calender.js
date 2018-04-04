function getCalenderData() {
    $.ajax({
        type: "get",
        dataType: "json",
        url: "/calender_data",
        async: true,
        contentType: "application/json",
        success: function (data) {
             Calender(data);
        },
        Error: function () {
            console.log("error");
        }
    });
}

function Calender(json) {
    console.log(json);

var width = 960,
    height = 200,
    cellSize = 17;

var formatPercent = d3.format(".1%");

var color = d3.scaleQuantize()
    .domain([0, 7])
    .range([ "#66bd63", "#d9ef8b", "#fdae61","#f46d43",
      "#d73027", "#a50026", "#330000"]);

var svg = d3.select("#Staynight")
  .selectAll("svg")
  .data(d3.range(2017, 2019))
  .enter().append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1-50) + ")");




svg.append("text")
    .attr("transform", "translate(-6," + cellSize * 3.5 + ")rotate(-90)")
    .attr("font-family", "sans-serif")
    .attr("font-size", 20)
    .attr("stroke","rgb(49, 130, 189)")
    .attr("text-anchor", "middle")
    .text(function(d) { return d; });

  var timeFormatSet=d3.timeFormat("%Y/%m/%d");

  var tooltip = d3.select("body").append("div").attr("class", "toolTip");

var rect = svg.append("g")
    .attr("fill", "none")
    .attr("stroke", "#ccc")
    .selectAll("rect")
    .data(function(d) {   return d3.timeDays(new Date(d, 0, 1), new Date(d + 1, 0, 1));        })
    .enter().append("rect")
    .attr("width", cellSize)
    .attr("height", cellSize)
    .attr("x", function(d) { return d3.timeWeek.count(d3.timeYear(d), d) * cellSize; })
    .attr("y", function(d) { return d.getDay() * cellSize; })
    .datum(d3.timeFormat("%Y-%m-%d"))
    .on('mouseover',function(d){
         //console.log(d.date);
           tooltip
          .style("left", d3.event.pageX-50+"px" )
          .style("top",  d3.event.pageY-50+"px" )
          .style("display", "inline-block")
          .html(d.date);
    })
    .on('mouseout',function(d){
      tooltip.style("display", "none");
    });

   //   console.log(rect,function(d){return d;})

svg.append("g")
    .attr("fill", "none")
    .attr("stroke", "#000")
    .selectAll("path")
    .data(function(d) { return d3.timeMonths(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
    .enter().append("path")
    .attr("d", pathMonth);


var data = d3.nest()
      .key(function(d) { return d.date; })
      .rollup(function(d) { return d.level; })
    .object(json);


  //.filter(function(d) { return d in data; })
    rect.data(json)
    .attr("fill", function(d) {return color(d.level); });

 var t=[1,2,3,4,5,6,7];
    var liangji=d3.select("#Staynight").select("svg")
                    .append("g")
                    .attr("class","liangji")
                    .attr("fill", "none")
                    .attr("stroke", "#ccc")
                    .selectAll("rect")
                    .data(t)
                    .enter()
                    .append("rect")
                    .attr("width",20)
                    .attr("height",20)
                    .attr("fill",function(d){
                      return color(d-1);
                    })
                    .attr("x",function(d){return d*30+10;})
                    .attr("y",160);

    var liangjiText=d3.select(".liangji")
                            .selectAll("text")
                            .data(t)
                            .enter()
                            .append("text")
                            .text(function(d){
                              if (d==7)
                                return d+"    "+"Hours/Day(Stay Night)";
                              else
                                return d;})
                            .attr("font-size","12px")
                            .attr("x",function(d){return d*30+15;})
                            .attr("y",195);


}


function pathMonth(t0) {
var cellSize=17;
  var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
      d0 = t0.getDay(),
      w0 = d3.timeWeek.count(d3.timeYear(t0), t0),
      d1 = t1.getDay(),
      w1 = d3.timeWeek.count(d3.timeYear(t1), t1);

  return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
      + "H" + w0 * cellSize + "V" + 7 * cellSize
      + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
      + "H" + (w1 + 1) * cellSize + "V" + 0
      + "H" + (w0 + 1) * cellSize + "Z";
}

getCalenderData();