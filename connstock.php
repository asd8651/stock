<?php
session_start();
$link = mysql_connect("0.tcp.ngrok.io:12714","root","ncutim")or die ("conn fail");
mysql_select_db('onmarket',$link) or die ("DB fail");
mysql_query("SET NAMES 'utf-8'");
mysql_query("SET CHARACTER_SET_CLIENT=utf-8");
mysql_query("SET CHARACTER_SET_RESULTS=utf8");
#for($q = 1000;$q < 9000;$q++){
$sqllimit="SELECT * FROM `1101`; ";
$result = mysql_query($sqllimit) or die ('mySQL query error');
while($row = mysql_fetch_array($result, MYSQL_NUM)){
    for($q=1;$q<9;$q++) {
        echo $row[$q];
    }
    }
?>
<html>
<head>
    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
    <script src="https://code.highcharts.com/stock/highstock.js"></script>
    <script src="https://code.highcharts.com/stock/modules/drag-panes.js"></script>
    <script src="https://code.highcharts.com/stock/modules/exporting.js"></script>
<body>



<div id="container" style="height: 400px; min-width: 310px"></div>
<script>
    function (data) {
        // split the data set into price and volume
        var price = [],
            volume = [],
            dataLength = data.length,
            // set the allowed units for data grouping
            groupingUnits = [[
                'week',                         // unit name
                [1]                             // allowed multiples
            ], [
                'month',
                [1, 2, 3, 4, 6]
            ]],

            i = 0;

        for (i; i < dataLength; i += 1) {
            price.push([
                data[i][0], // the date
                data[i][1], // open
                data[i][2], // high
                data[i][3], // low
                data[i][4] // close
            ]);

            volume.push([
                data[i][0], // the date
                data[i][5] // the volume
            ]);
        }


        // create the chart
        Highcharts.stockChart('container', {

            rangeSelector: {
                selected: 1
            },

            title: {
                text: '2330台積電'
            },

            yAxis: [{
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: '2330'
                },
                height: '60%',
                lineWidth: 2,
                resize: {
                    enabled: true
                }
            }, {
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'Volume'
                },
                top: '65%',
                height: '35%',
                offset: 0,
                lineWidth: 2
            }],

            tooltip: {
                split: true
            },

            series: [{
                type: 'candlestick',
                name: '台積電',
                data: price,
                dataGrouping: {
                    units: groupingUnits
                }
            }, {
                type: 'column',
                name: 'Volume',
                data: volume,
                yAxis: 1,
                dataGrouping: {
                    units: groupingUnits
                }
            }]
        });
    });
</script>
</body>
</head>
</html>