function pieChart(data) {

    d3.select("#pie_svg").remove();

    var history = data;
    // console.log(history);

    var pie_rect = $("#pie_view");

    var width=pie_rect.width();
    var height=pie_rect.height();

    var svg=d3.select("#pie_view")
            .append("svg")
            .attr("id","pie_svg")
            .attr("width",width)
            .attr("height",height);

    svg.selectAll("g").remove();


	var pie=d3.pie().value(function(d,i){return d.count;});

    var piedata=pie(history);

    //console.log(piedata);

    var outerRadius=width/3;
    var innerRadius=outerRadius;

    var arc=d3.arc()
                    .innerRadius(innerRadius/2)
                    .outerRadius(outerRadius);

    var color = d3.scaleOrdinal(d3.schemeCategory20c);



    var arcs=svg.selectAll("g")
                    .data(piedata)
                    .enter()
                    .append("g")
                    .attr("transform","translate("+(width/2)+","+(height/2-height/8)+")");
    var tooltip = d3.select("body").append("div").attr("class", "toolTip");


    arcs.append("path")
        .attr("fill",function(d,i){
            return color(i);
        })

        .attr("d",function(d){
            return arc(d);
        })
        .on("mouseover",function(d,i){
            d3.select(this)
                .transition()
                .duration(500)
                .attr("fill","#c2b7b7");
            tooltip
              .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
                    .html(d.data.url+"<br>"+d.value);
              })
        .on("mouseout",function(d,i){
            d3.select(this)
                .transition()
                .duration(500)
                .attr("fill",color(i));
            tooltip.style("display", "none");
        });




    arcs.append("text")
        .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")rotate(" + angle(d) + ")"; })
        .attr("text-anchor","middle")
        .text(function(d,i){
            var percent=Number(d.value)/d3.sum(history,function(d,i){return d.count;})*100;
            if (percent>3)
            return percent.toFixed(0)+"%";
        });



    var right=piedata.splice(0,5);
    var left = piedata.splice(0,5);
    //console.log(right);

    var biaozhi=d3.select("#pie_svg")
                  .append("g")
                  .attr("class","biaozhi")
                  .attr("fill", "none")
                  .attr("stroke", "#ccc")
                  .selectAll("rect")
                  .data(right)
                  .enter()
                  .append("rect")
                  .attr("width",20)
                  .attr("height",20)
                  .attr("fill",function(d,i){
                      return color(i);
                  })
                  .attr("x", 10)
                  .attr("y",function(d,i){return i*25+(height-150);});

    var liangjiText=d3.select(".biaozhi")
                      .selectAll("text")
                      .data(right)
                      .enter()
                      .append("text")
                      .text(function(d){
                         return d.data.url;
                      })
                      .style("stroke-width",1)
                      .style("stroke",function(d,i){
                          return color(i);
                      })
                      .style("font-size",12)
                      .attr("x", 40)
                      .attr("y",function(d,i){return i*25+(height-135);});

    var paddingright = width/2;

    var biaozhix=d3.select("#pie_svg")
                          .append("g")
                          .attr("class","biaozhix")
                          .attr("fill", "none")
                          .attr("stroke", "#ccc")
                          .selectAll("rect")
                           .data(left)
                          .enter()
                          .append("rect")
                          .attr("width",20)
                          .attr("height",20)
                          .attr("fill",function(d,i){
                            return color(i+5);
                          })
                          .attr("x", paddingright)
                          .attr("y",function(d,i){return i*25+(height-150);});

    var liangjiTextx=d3.select(".biaozhix")
                            .selectAll("text")
                            .data(left)
                            .enter()
                            .append("text")
                            .text(function(d){
                              return d.data.url;
                            })
                            .style("stroke-width",1)
                            .style("stroke",function(d,i){
                                 return color(i+5);
                            })
                            .style("font-size",12)
                            .attr("x", paddingright + 30 )
                            .attr("y",function(d,i){return i*25+(height-135);});

    d3.select("#pie_svg")
           .append("text")
           .text("Top 10 websites")
           .attr("font-size","20px")
           .attr("x",10)
           .attr("y",20);

    function angle(d) {
        var a = (d.startAngle + d.endAngle) * 90 / Math.PI - 90;
        return a > 90 ? a - 180 : a;
    }



}