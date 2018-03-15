function transmitDataPie(data) {
     $.ajax({
            type:'POST',
            url:"/brush_data",
            data:JSON.stringify(data),
            contentType:'application/json',
            dataType:'json',
            success:function(data){
                // alert(JSON.stringify(data));
                pieChart(data);
                console.log(data);
            }
        });
}

function transmitDataRadar(data) {
     $.ajax({
            type:'POST',
            url:"/radar_data",
            data:JSON.stringify(data),
            contentType:'application/json',
            dataType:'json',
            success:function(data){
                // alert(JSON.stringify(data));
                radarChart(data);
                console.log(data);
            }
        });
}

// function transmitDataBar(data) {
//      $.ajax({
//             type:'POST',
//             url:"/bar_data",
//             data:JSON.stringify(data),
//             contentType:'application/json',
//             dataType:'json',
//             success:function(data){
//                 // alert(JSON.stringify(data));
//                 barChart(data);
//                 console.log(data);
//             }
//         });
// }