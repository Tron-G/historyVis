function barChart(data) {
    var bar_view = $("#bar_view");
	  d3.select("#Daychart").remove();
      d3.select("#Weekchart").remove();
      d3.select("#Monthchart").remove();

            var months=[];
            var weeks=[];
            var days=[];
            var times;
            var num;
		 	for(var ob in data)
		 	{
		 		if(ob[0]=='w')
		 		{
		 			for(var i in data[ob])
		 			{
		 				switch (i)
				{
					case "MON": times=1; break;
					case "TUE": times=2;break;
					case "WED": times=3;break;
					case "THU": times=4;break;
					case "FRI": times=5;break;
					case "SAT": times=6;break;
					case "SUN": times=7;break;
				}
				weeks[times]=data[ob][i];
		 			}
		 		}
		 		else if(ob[0]=='d')
		 		{
		 			for(var i in data[ob])
		 			{
		 				num=Number(i);
		 				days[num]=data[ob][i];
		 			}
		 		}
		 		else{
		 			for(var i in data[ob])
		 			{
		 				num=Number(i);
		 				months[num]=data[ob][i];
		 			}
		 		}
		 	}

		 	draw(days,"Daychart");
 			draw(weeks,"Weekchart");
 			draw(months,"Monthchart");



 	function draw(dataset,AimSvg)
   	{
		    var rectPadding = 4;
		    var width=bar_view.width();
		    var height=(bar_view.height()-10)/3;
		    var padding={top:height*0.05,right:width*0.03,bottom:height*0.15,left:width*0.07};


		    var svg=d3.select("#bar_view")
		    			.append("svg")
		    			.attr("id",AimSvg)
		                .attr("width",width)
		                .attr("height",height);

		    svg.append("text")
		    		.text(function(){
		    			if (AimSvg == "Daychart") return "Time of Day";
		    			else if (AimSvg == "Weekchart")  return "Day of Week";
		    			else return "Day of Month";
		    		})
		    		.attr("font-size","15px")
		    		.attr("transform","translate("+45+","+15+")");


		    var xAxisWidth=width*0.9;
		    var yAxisWidth=height*0.8;
		    var xScale=d3.scaleBand()
		                        .domain(d3.range(1,dataset.length))
		                        .range([0,xAxisWidth])
		                        .round(true);

		    var yScale = d3.scaleLinear()
		                        .domain([0,d3.max(dataset)])
		                        .range([0,yAxisWidth]);

			var tooltip = d3.select("body").append("div").attr("class", "toolTip");
		    var rect=svg.selectAll("rect")
		                                .data(dataset)
		                                .enter()
		                                .append("rect")
		                                .attr("fill","rgb(107, 174, 214)")
		                                .attr("x",function(d,i){
		                                    return padding.left+xScale(i)+rectPadding/2;
		                                })
		                                .attr("y",function(d,i){
		                                    return height-padding.bottom-yScale(d);
		                                })
		                                .attr("width",width/dataset.length-rectPadding)
		                                .attr("height",function(d){
		                                    return yScale(d);
		                                })
								        .on('mouseover', function (d){
								        	 d3.select(this)
		                                            .transition()
		                                            .duration(500)
		                                            .attr("fill","rgb(253, 141, 60)");


								            tooltip
								              .style("left", d3.select(this).attr("x") + "px")
								              .style("top", d3.select(this).attr("y")+ "px")
								              .style("display", "inline-block")
								              .attr("fill", "white")
								      				.html(d);
								            })
								    		.on("mouseout", function(d){
 											 d3.select(this)
		                                        .transition()
		                                        .duration(500)
		                                        .attr("fill","rgb(107, 174, 214)");

								    			tooltip.style("display", "none");
								    	});

		     function Texttransform (y){
		     		if (AimSvg=="Daychart") return height*0.15;
		     		else if (AimSvg=="Weekchart") return height*1.1;
		     		else return height*2.1;
		     }

		    var xAxis=d3.axisBottom(xScale);


		    yScale.range([yAxisWidth,0]);

		    var yAxis=d3.axisLeft(yScale)
		    				.ticks(3);

		    svg.append("g").attr("class","axis")
		                    .attr("transform","translate("+padding.left+","+
		                        (height-padding.bottom)+")")
		                         .call(xAxis);


		    svg.append("g").attr("class","axis")
		                    .attr("transform","translate("+padding.left+","+
		                        (height-yAxisWidth-padding.bottom)+")")
		                    .call(yAxis);

		   var s=svg.selectAll(".axis").selectAll(".line")
		   						.attr("fill","none");

		}

}