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

    //純json 格式
    if (empty($_GET[$jsonp_callback_key]))
    {
        return $encode;
    }

    //jsonp 方法
    return "{$jsonp_get}($encode)";
}

?>
<!DOCTYPE html>
<html>
<head>
    <script src="jquery.js"></script>
    <script src="highcharts.js"></script>
    <script src="highcharts-more.js"></script>
    <link href="chartsss.css" type="text/css" rel="stylesheet">
    <meta http-equiv="Content-Type" content="text/html; charset=big5-hkscs">
    <div id="container" style="min-width:600px;height:400px">
    <script>
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
        function activeLastPointToolip(chart) {
            var points = chart.series[0].points;
            chart.tooltip.refresh(points[points.length -1]);
        };
        $(function () {
            $.getJSON('http://60.249.6.104:8787/api/get/3/data/realtime', function (data) {
                var _data = data;
                console.log(_data);
                var pv_volt = _data['pv_volt'], pv_cur = _data['pv_cur'], pv_power = _data['pv_power'],
                    Rediation = _data['Rediation'], pv_Temp = _data['pv_Temp'],amb_temp = _data['amb_temp'],
                    Daily = _data['Daily'], total_L = _data['total_L'], total_H = _data['total_H'];
                //var chart = Highcharts.chart('container', {
                dataArray = new Array();
                for(w in _data)
                {
                    console.log(w);
                    console.log(_data[w]);
                }
                var chart = $('#container').highcharts({
                    chart: {
                        type: 'spline',
                        animation: Highcharts.svg, // don't animate in old IE
                        marginRight: 140,
                        events: {
                            load: function () {
                                var label = this.renderer.label('載入中，請稍候', 100, 120)
                                    .attr({
                                        fill: Highcharts.getOptions().colors[0],
                                        padding: 10,
                                        r: 5,
                                        zIndex: 8
                                    });
                                var series = this.series[0],
                                    chart = this;
                                setInterval(function () {
                                    var x = (new Date()).getTime(), // current time
                                        y = amb_temp;
                                    series.addPoint([x, y], true, true);
                                    activeLastPointToolip(chart)
                                }, 10000);
                            }
                        }
                    },
                    title: {
                        text: ''
                    },
                    xAxis: {
                        type: 'datetime',
                        tickPixelInterval: 200
                    },
                    yAxis: {
                        title: {
                            text: '值'
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
                        itemHoverStyle: {
                            color:'pink'
                        },
                        align: 'right',
                        verticalAlign: 'top',
                        layout: 'vertical',
                        itemMarginBottom:10,
                        itemMarginTop:13,
                        symbolPadding:10,
                        reversed: true,
                        shadow: true,
                        x:0,
                        width:100

                    },
                    exporting: {
                        enabled: false
                    },
                    series: [{
                        name: 'pv_volt',
                        data: (function () {
                            var data = [],
                                time = (new Date()).getTime(),
                                i;
                            for (i = -19; i <= 0; i+=1) {
                                data.push({
                                    x: time + i * 10000,
                                    y: pv_volt
                                });
                            }
                            return data;
                        }())
                    },{
                        name: 'pv_cur',
                        data: (function () {
                            var data = [],
                                time = (new Date()).getTime(),
                                i;
                            for (i = -19; i <= 0; i+=1) {
                                data.push({
                                    x: time + i * 10000,
                                    y: pv_cur
                                });
                            }
                            return data;
                        }())
                    },{
                        name: 'pv_power',
                        data: (function () {
                            var data = [],
                                time = (new Date()).getTime(),
                                i;
                            for (i = -19; i <= 0; i+=1) {
                                data.push({
                                    x: time + i * 10000,
                                    y: pv_power
                                });
                            }
                            return data;
                        }())
                    },{
                        name: 'Rediation',
                        data: (function () {
                            var data = [],
                                time = (new Date()).getTime(),
                                i;
                            for (i = -19; i <= 0; i+=1) {
                                data.push({
                                    x: time + i * 10000,
                                    y: Rediation
                                });
                            }
                            return data;
                        }())
                    },{
                        name: 'pv_Temp',
                        data: (function () {
                            var data = [],
                                time = (new Date()).getTime(),
                                i;
                            for (i = -19; i <= 0; i+=1) {
                                data.push({
                                    x: time + i * 10000,
                                    y: pv_Temp
                                });
                            }
                            return data;
                        }())
                    },{
                        name: 'amb_Temp',
                        data: (function () {
                            var data = [],
                                time = (new Date()).getTime(),
                                i;
                            for (i = -19; i <= 0; i+=1) {
                                data.push({
                                    x: time + i * 10000,
                                    y: amb_temp
                                });
                            }
                            return data;
                        }())
                    },{
                        name: 'Daily',
                        data: (function () {
                            var data = [],
                                time = (new Date()).getTime(),
                                i;
                            for (i = -19; i <= 0; i+=1) {
                                data.push({
                                    x: time + i * 10000,
                                    y: Daily
                                });
                            }
                            return data;
                        }())
                    },{
                        name: 'total_H',
                        data: (function () {
                            var data = [],
                                time = (new Date()).getTime(),
                                i;
                            for (i = -19; i <= 0; i+=1) {
                                data.push({
                                    x: time + i * 10000,
                                    y: total_H
                                });
                            }
                            return data;
                        }())
                    }]
                }, function (c) {
                    activeLastPointToolip(c)
                });
            });
        });
        </script>
    </div>
    <title>測試</title>
</head>
</html>
