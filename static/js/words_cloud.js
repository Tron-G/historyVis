function wordsCloud(dataset) {

    console.log(dataset);
    var chart = echarts.init(document.getElementById('wordcloud'));

    var newdata = new Array();
    for(var i=0;i<dataset.length;i++){
        newdata[i] = new Object();
        newdata[i].name = dataset[i].name;
        newdata[i].value = dataset[i].value;
    }

    var cloud_rect = $("#wordcloud");
    var width=cloud_rect.width();
    var height=cloud_rect.height();

    var option = {
        tooltip: {},
        series: [ {
            type: 'wordCloud',
            gridSize: 2,
            sizeRange: [20, 60],
            rotationRange: [-90, 90],
            shape: 'pentagon',
            width: width,
            height: height,
            drawOutOfBound: true,
            textStyle: {
                normal: {
                    color: function () {
                        return 'rgb(' + [
                            Math.round(Math.random() * 160),
                            Math.round(Math.random() * 160),
                            Math.round(Math.random() * 160)
                        ].join(',') + ')';
                    }
                },
                emphasis: {
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            },
            data:[]
        } ]
    };
    option.series[0].data = newdata;

    console.log(option.series[0].data);

    chart.setOption(option);

    window.onresize = chart.resize;
}

 // d3.csv("../static/words.csv",function (error,data) {
 //     if(error) throw error;
 //     var words = data;
 //     console.log(words);
 //     wordsCloud(words);
 // });
