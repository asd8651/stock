<?php
header("Content-Type:text/html; charset=big5-hkscs");
header('Access-Control-Allow-Origin:*');
header('Access-Control-Allow-Methods: GET, POST, PUT');
header('Access-Control-Allow-Headers: Content-Type');
function json($data)
{
    $encode               = json_encode($data);
    $jsonp_callback_key   = 'callback';
    $jsonp_get            = $_GET[$jsonp_callback_key];

    //��json �榡
    if (empty($_GET[$jsonp_callback_key]))
    {
        return $encode;
    }

    //jsonp ��k
    return "{$jsonp_get}($encode)";
}

?>
<!DOCTYPE html>
<html>
<head>
    <script src="jquery.js"></script>
    <script src="highcharts.js"></script>
    <link href="chartsss.css" type="text/css" rel="stylesheet">
    <meta http-equiv="Content-Type" content="text/html; charset=big5-hkscs">
    <div id="container" style="min-width:400px;height:400px">
    <script>

        var outside;
        $.ajax({
            type: 'GET',                     //GET or POST
            url: "http://60.249.6.104:8787/api/get/GC1EbTQckPZG/data/realtime",  //�ШD������
            cache: false,   //�O�_�ϥΧ֨�
            dataType:'json',
            success: function(result){   //�B�z�^�Ǧ��\�ƥ�A��ШD���\�ᦹ�ƥ�|�Q�I�s
                //var myObj = $.parseJSON(result);
                //console.log("AC output voltage: "+result["AC output voltage"]);
                outside=result;
            },
            error: function(result){   //�B�z�^�ǿ��~�ƥ�A��ШD���ѫᦹ�ƥ�|�Q�I�s
                console.log('fail');
            },   //your code here
            complete: function(result){
                a();
            },
            statusCode: {                     //���A�X�B�z
                404: function() {
                    alert("page not found");
                }
            }
        });
        function a() {
            console.log(outside['AC output voltage'])
        }
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
        function activeLastPointToolip(chart) {
            var points = chart.series[0].points;
            chart.tooltip.refresh(points[points.length -1]);
        }
        $('#container').highcharts({
            chart: {
                type: 'spline',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function () {
                        // set up the updating of the chart each second
                        var series = this.series[0],
                            chart = this;
                        setInterval(function () {
                            var x = (new Date()).getTime(), // current time
                                y = Math.random();
                            series.addPoint([x, y], true, true);
                            activeLastPointToolip(chart)
                        }, 1000);
                    }
                }
            },
            title: {
                text: '�ʺA����'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: '��'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: '�H���ƾ�',
                data: (function () {
                    // generate an array of random data
                    var data = [],
                        time = (new Date()).getTime(),
                        i;
                    for (i = -19; i <= 0; i += 1) {
                        data.push({
                            x: time + i * 1000,
                            y: Math.random()
                        });
                    }
                    return data;
                }())
            }]
        }, function(c) {
            activeLastPointToolip(c)
        });
    </script>
    </div>
    <title>����</title>
</head>
</html>
