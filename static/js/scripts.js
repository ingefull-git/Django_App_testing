
    $(function () {
        var url = $("#searchform").attr('action');
        var token = jQuery("[name = csrfmiddlewaretoken]").val();

        $("#searchform").submit(function (e) {
            e.preventDefault(e);
            var formData = $("form").serializeArray();
            var cant = 0;
            $.ajax({
                    url: url,
                    method: "POST",
                    headers: {
                        'X-CSRFToken': token
                    },
                    data: {
                        formData,
                        'searchfield': "searchfield"
                    },
                })
                .done(function (data, textStatus, xhr) {
                    if (xhr.status == 200) {
                        $("#tablebody").html("")
                        $.each(data, function (k, v) {
                            $("#tablebody").append('<tr><td>' + cant + '</td><td>' + data[k].name + '</td><td>' + data[k].psid + '</td><td>' + data[k].status + '</td><td> <a href="#" class="btn btn-primary btn-sm" >Update</a> </td></tr>');
                            cant++
                        });
                    } else {
                        console.log("Funcion .done pero no status=200")
                    }
                })
                .fail(function (data) {
                    console.log("Fail..!!: ", data)
                })
        });
    });




    var $pie_chart = $("#myChart");

$.ajax({
    method: "GET",
    url: $pie_chart.data("url"),
    data: {
        'refresh': "refreshchart"
    },
    success: function (data) {

        let canvas = document.getElementById("myChart");
        let ctx = canvas.getContext('2d');
        let myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        '#FF474B',
                        '#FEE043',
                        '#649CB8',
                        '#58AB51',
                    ],
                    borderWidth: 1
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
            },
        });
        canvas.onclick = function (evt) {
            let activePoints = myChart.getElementsAtEventForMode(evt, 'nearest', {
                intersect: true
            }, true);
            if (activePoints.length) {
                activePoints.forEach((p) => {
                    let label = myChart.data.labels[p.index];
                    let value = myChart.data.datasets[p.datasetIndex].data[p.index];
                    console.log(`label: _[${label}]_, value: [${value}] cant`);
                    let url = "http://127.0.0.1:8000/chart_detail/" + label + "/";
                    console.log(url);
                    modal_generic(url);

                    // alert(url);
                })
            };

        };
        $('#a_tag_log').on("click", function () {

            $.ajax({
                method: "GET",
                url: $pie_chart.data("url"),
                data: {
                    'psid': 1111
                },
                success: function (data) {
                    console.log("A tag Btn..!!", data.values)
                    myChart.data.datasets[0].data = data.values;

                    myChart.update();
                    refresh_home();
                },
            });
        });

    }
});



    $(document).ready(function () {
        refresh_home();
    });



    function refresh_home() {
        $.ajax({
            url:'/',
            type: 'GET',
            data: {
                'refresh': "refreshpage",
            },
            success: function (data) {
                buildTable(data);
           },
            error: function(){
                alert("failure..!!!");
            }
       });
      };

    function buildTable(data){
        var cant = 0;
        var html = "";
            
        $("#tablebody").html("")
                    $.each(data, function (k,v) {
                        $("#tablebody").append('<tr><td>' + cant + '</td><td>'+ data[k].name + '</td><td>' + data[k].psid + '</td><td>' + data[k].status + '</td><td> <a href="#" class="btn btn-primary btn-sm" >Update</a> </td></tr>');
                        cant++;
                    });
    };



    function modal_generic(url) {
        $('#modalGeneric').load(url, function () {
            $(this).modal('show');
        });
    };
