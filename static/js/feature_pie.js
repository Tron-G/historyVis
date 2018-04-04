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
	var daytime=$("#daytime");
	var day_section=new Array();
	//console.log(data);
    for(var i in data)
    {
    	var section={};
    	for(var j in data[i])
    	{
    		switch(j)
    		{
    			case "scale": section.scale=data[i][j];break;
    			case "section": section.section=data[i][j];break;
    			case "sort": section.sort=data[i][j];break;
    			case "visit_count": section.times=data[i][j];break;
    		}
    	}
    	day_section.push(section);
    }
    var width = daytime.width()*0.8,
    height = daytime.height()*0.85,
    radius = Math.min(width, height) / 2,
    innerRadius = 0.4 * radius;

    var svg=d3.select("#daytime")
                .append("svg")
                .attr("width",daytime.width())
                .attr("height",daytime.height())
                .attr("transform", "translate(" + daytime.width()*0.2 + "," + 0 + ")");


        var x=d3.scaleLinear()
                  .domain([d3.min(day_section,function(d){return d.times;}),
                        d3.max(day_section,function(d){return d.times;})])
                  .range([5,70]);



    var pie=d3.pie()
            .sort(comparex)
            .value(function(d,i){return d.scale;});


 var comparex = function (val1, val2)
                  {

                          if (val1.sort < val2.sort) {
                              return -1;
                          } else if (val1.sort > val2.sort) {

                              return 1;
                          } else {
                              return 0;
                          }
                   }



    var arc=d3.arc()
                    .innerRadius(innerRadius)
                    .outerRadius(function (d) {
    return ((innerRadius) * (d.data.scale / 50.0) + innerRadius);
  });


    var color = d3.scaleOrdinal(d3.schemeCategory20c);



   // console.log(day_section);
    var arcs=svg.selectAll("g")
                    .data(pie(day_section))
                    .enter()
                    .append("g")
                    .attr("transform","translate("+radius+","+(radius+daytime.height()*0.07)+")");

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
              .style("left", d3.event.pageX -30+ "px")
              .style("top", d3.event.pageY - 60 + "px")
              .style("display", "inline-block")
               .html(d.data.section+"<br>"+d.data.times);
              })
            .on("mouseout",function(d,i){
                d3.select(this)
                    .transition()
                    .duration(500)
                    .attr("fill",color(i));
                    tooltip.style("display", "none");

                });

            //console.log(day_section);
        var biaozhi=d3.select("#daytime").select("svg")
                      .append("g")
                      .attr("class","biaozhi")
                      .attr("fill", "none")
                      .attr("stroke", "#ccc")
                      .selectAll("rect")
                      .data(day_section)
                      .enter()
                      .append("rect")
                      .attr("width",20)
                      .attr("height",20)
                      .attr("fill",function(d,i){
                        return color(i);
                      })
                      .attr("x", 310)
                      .attr("y",function(d,i){return i*25+80;});


        var liangjiText=d3.select(".biaozhi")
                            .selectAll("text")
                            .data(day_section)
                            .enter()
                            .append("text")
                            .text(function(d){
                              return d.section;
                            })
                            .style("stroke-width",1)
                            .style("stroke",function(d,i){
                        return color(i);
                      })
                            .style("font-size",12)
                            .attr("x", 335)
                            .attr("y",function(d,i){return i*25+93;});


        d3.select(".biaozhi").append("text")
                            .text("Time Of Day")
                            .style("stroke-width",1)
                            .style("stroke" ,"black")
                            .style("font-size",12)
                            .attr("x", 310)
                            .attr("y",70);



        return day_section;
    
}
getPiesData();