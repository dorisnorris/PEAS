$(function () {
    $('.selectpicker').selectpicker();
});

$('#SelectPlanet').on('change',function(){
    console.log("HELLO");
    // get multi select values 
    var selected = $('#SelectPlanet').find("option:selected"); //get current selected value
    var arrSelectedPlanet = []; //Array to store your multiple value in stack
    selected.each(function(){
    arrSelectedPlanet.push($(this).val()); //Stack the value
    });

// $('#SelectPlanet').on('change',function(){
    console.log(arrSelectedPlanet);

    $.ajax({
        url: "/planet", 
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected_planet': JSON.stringify(arrSelectedPlanet)
        },
        dataType:"json",
        success: function (data) {
            Plotly.newPlot('flux_plot', data );
        }
    });
})

