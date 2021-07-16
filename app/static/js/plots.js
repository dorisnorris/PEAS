$('#SelectPlanet').on('change',function(){
    $.ajax({
        url: "/<plnt>", 
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'planet': document.getElementById('SelectPlanet').value,
        },
        dataType:"json",
        success: function (data) {
            Plotly.newPlot('flux_plot', data );
        }
    });
})