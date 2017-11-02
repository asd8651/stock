<?php
//session_start();
//$link = mysql_connect("0.tcp.ngrok.io:12714","root","ncutim")or die ("conn fail");
//mysql_select_db('onmarket',$link) or die ("DB fail");
//mysql_query("SET NAMES 'utf-8'");
//mysql_query("SET CHARACTER_SET_CLIENT=utf-8");
//mysql_query("SET CHARACTER_SET_RESULTS=utf8");
//$sqllimit="SELECT * FROM `1540`; ";
//$result = mysql_query($sqllimit) or die ('mySQL query error');
//while($row = mysql_fetch_array($result)) {
//    echo $row['ID'];
//}
//?>

<!DOCTYPE html>
<html>
<head>
    <script src="jquery.js"></script>
    <script src="highcharts.js"></script>
    <link href="chartsss.css" type="text/css" rel="stylesheet">
    <div id="Header"></div>
    <div id="Sidebar"></div>
    <div id="container" style="min-width: 310px; height: 400px; margin: 0 auto">
        <script>
            function opt1() {
                var opt = document.type.selectedIndex;
                if (opt.value==1){
                    alert(a);
                }
            }
            var day = ['2017/10/14','2017/10/15','2017/10/16','2017/10/17'];
            var view = [300,150,100,200];
            var eqw = [30,15,10,20];
            Highcharts.chart('container', {
                chart: {
                    type: 'area'
                },
                title: {
                    text: '簡單每日人氣表'
                },
                subtitle: {
                    text: 'Source: never-nop.com'
                },
                xAxis: {
                    maxpadding: 0.6,
                    categories:day,
                    tickmarkPlacement: 'on',
                    title: {
                        enabled: false
                    }
                },
                yAxis: [{
                    title: {
                        text: 'Voltage'
                    },
                    labels: {
                        formatter: function () {
                            return this.value
                        },
                        showFirstLabel: true
                    }
                },{
                    itle: {
                        text: null
                    },
                    labels: {
                        formatter: function () {
                            return this.value
                        },
                        showFirstLabel: false
                    }

                }],
                tooltip: {
                    split: true,
                    valueSuffix: ' V'
                },
                plotOptions: {
                    area: {
                        stacking: 'normal',
                        lineColor: '#666666',
                        lineWidth: 1,
                        marker: {
                            lineWidth: 1,
                            lineColor: '#666666'
                        }
                    }
                },
                series: [{
                    name: 'voltage',
                    data: view
                },{
                    name: '987',
                    data: eqw
                }
                ]
            });
        </script>
    </div>
    <div style='clear:both;'></div>
    <div id="Footer">Footer 欄位</div>
    <!--<link rel=stylesheet type="text/css" href="cha.css">-->
    <meta charset="utf-8">
    <title>測試</title>

<body>


<select name="type" class="opts" id="type" onchange="opt1()">
    <option selected value="1">折線圖</option>
    <option value="2">圓餅圖</option>
    <option value="3">柱狀圖</option>
</select>
<select id="data"name="data" class="opts" >
    <option  value="4">電壓</option>
    <option value="5">電流</option>
    <option value="6">溫度</option>
</select>
<button type="button" onclick="displayResult()">show!</button>


</body>
</head>
</html>
