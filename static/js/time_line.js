function timeLine(data) {

    var time_line = $("#brush_view");
    var select_time = [];
      // console.log(data);
    var time_svg = d3.select("#brush_view").append("svg")
            .attr("id","time_svg")
            .style("position", "absolute")
            .attr("width", time_line.width())
            .attr("height", time_line.height());

      // slider
      var sliderHeight= time_line.height() - 20;
      var sliderWidth = time_line.width() - 20;

      // console.log(sliderWidth);
      var sliderMargin = {
        "top" : sliderHeight*0.8,
        "bottom" : 5,
        "left" : 10,
        "right" : 10
      };

      var time_format = d3.timeFormat("%Y/%m/%d");

      var begin_time = new Date(data[0].lastVisitTime.split("/"));
      var end_time = new Date(data[data.length-1].lastVisitTime.split("/"));

      var xYearFirst = d3.scaleTime()
                .domain([begin_time, end_time])
                .range([0, sliderWidth])
                .clamp(true);

      // var  x2 = d3.scaleTime().range([0, sliderWidth]);

      var sliderYearFirst = time_svg.append("g")
          .attr("class", "slider")
          .attr("transform", "translate(" + sliderMargin.left + "," + sliderMargin.top + ")");

      sliderYearFirst.append("line")
          .attr("class", "track")
          .attr("x1", xYearFirst.range()[0])
          .attr("x2", xYearFirst.range()[1]);


      sliderYearFirst.insert("g")
          .attr("class", "ticks")
          .attr("transform", "translate(0," + 18 + ")")
          .selectAll("text")
          .data(xYearFirst.ticks(5))
          .enter().append("text")
          .attr("font-size", "10px")
          .attr("x", xYearFirst)
          .attr("text-anchor", "middle")
          .text(function(d) { return time_format(d); });


    //文字--------------------------------------------------------------------------
      var time_range = [sliderWidth*0.05,sliderWidth-sliderWidth*0.05];

      var svgFilterText = time_svg
          .insert("g")
          .selectAll("text")
          .data([0,1])
          .enter()
          .append("text");

      var svgFilterLabels =  svgFilterText
          .attr("x", function(d) { return time_range[d]; })
          .attr("y", sliderMargin.top+sliderMargin.top*0.25)
          .text( function (d) { return 0; })
          .attr("font-family", "sans-serif")
          .attr("font-size", "15px")
          .attr("font-weight","bold");

      var svgFilterDesc = time_svg
          .insert("g")
          .selectAll("text")
          .data([2])
          .enter()
          .append("text");


    //刷子----------------------------------------------------------------------------
    var x = d3.scaleTime().range([0, sliderWidth]),
        x2 = d3.scaleTime().range([0, sliderWidth]),
        y = d3.scaleLinear().range([sliderHeight/2, 0]),
        y2 = d3.scaleLinear().range([sliderHeight/2,0]);

    // console.log(sliderHeight/2);

    var area2 = d3.area()
        .curve(d3.curveMonotoneX)
        .x(function(d) { return x2(new Date(d.lastVisitTime.split("/"))); })
        .y0(y(0))
        .y1(function(d) {
           // console.log(d.visitCount,y2(d.visitCount));
            return y2(d.visitCount); });


      x.domain(d3.extent(data, function(d) { return new Date(d.lastVisitTime.split("/")); }));
      y.domain([0, d3.max(data,function (d) {
          return d.visitCount;
      })]);
      x2.domain(x.domain());
      y2.domain(y.domain());


    var brush = d3.brushX()
        .extent([[0, 0], [sliderWidth, sliderHeight/2]])
        .on("brush", function(){
         updateFilterText();
        })
        .on("end", function(){
            select_time = getRangeText();

             var post_time = {};
                post_time.beginTime = select_time[0];
                post_time.endTime = select_time[1];

                transmitDataPie(post_time);               //数据传输
                transmitDataRadar(post_time);
                transmitDataBar(post_time);
          // console.log(getRangeText());
        });


    time_svg.append('g')
           .attr("transform", "translate(" + sliderMargin.left+"," +sliderMargin.top/4+")")
          .append("path")
          .attr("class", "area")
          .attr("d", area2(data));


      time_svg.append("g")
          .attr("class", "brush")
          .call(brush)
          .call(brush.move, x.range())
          .attr("transform", "translate(" + sliderMargin.left+"," +sliderMargin.top/4+")");

            var handle1 = time_svg.select(".brush").select(".handle--w");
            // console.log(handle1.attr("x"));
            var handle2 = time_svg.select(".brush").select(".handle--e");

    //   function brushed() {
    //   var s = d3.event.selection || x2.range();
    //   x.domain(s.map(x2.invert, x2));
    // }

      function getRangeText() {
          var handle1 = time_svg.select(".brush").select(".handle--w");
            //console.log(handle1.attr("x"));
          var handle2 = time_svg.select(".brush").select(".handle--e");

          var valA = xYearFirst.invert(handle1.attr("x"));
          var valB = xYearFirst.invert(Math.ceil(handle2.attr("x"))+3);

          // console.log(time_format(valA),time_format(valB));
          return [time_format(valA),time_format(valB)];
      }

      function updateFilterText() {
          var data = getRangeText();
        //console.log(data);
        var valA = +data[0];
        var valB = +data[1];
        redrawLabel(data);
      }

      function redrawLabel(curVal) {
        //console.log(svgFilterText);
        svgFilterLabels
          .text(function(d) { return curVal[d]; })
  }

}