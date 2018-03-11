function transmitData(data) {
     $.ajax({
            type:'POST',
            url:"/brush_data",
            data:JSON.stringify(data),
            contentType:'application/json',
            dataType:'json',
            success:function(data){
                // alert(JSON.stringify(data));
                console.log(data);
            }
        });
}