<?php
print_r($_GET['code']);
session_start();
$link = mysql_connect("0.tcp.ngrok.io:12714","root","ncutim")or die ("conn fail");
mysql_select_db('onmarket',$link) or die ("DB fail");
mysql_query("SET NAMES 'utf-8'");
mysql_query("SET CHARACTER_SET_CLIENT=utf-8");
mysql_query("SET CHARACTER_SET_RESULTS=utf8");
/*$sqllimit="SELECT * FROM `".$_GET['code']."`where date = ".date("Y/m/d")."; ";*/
$sqllimit="SELECT * FROM `".$_GET['code']."`where id = 1; ";
$result = mysql_query($sqllimit) or die ('mySQL query error');
echo "<table border='1'>
<tr>
<th>ID</th>
<th>date</th>
<th>sid</th>
<th>name</th>
<th>shareTrades</th>
<th>turnover</th>
<th>open</th>
<th>high</th>
<th>low</th>
<th>closing</th>
</tr>";

while($row = mysql_fetch_array($result))
{
    echo "<tr>";
    echo "<td>" . $row['1'] . "</td>";
    echo "<td>" . $row['date'] . "</td>";
    echo "<td>" . $row['sid'] . "</td>";
    echo "<td>" . $row['name'] . "</td>";
    echo "<td>" . $row['shareTrades'] . "</td>";
    echo "<td>" . $row['turnover'] . "</td>";
    echo "<td>" . $row['open'] . "</td>";
    echo "<td>" . $row['high'] . "</td>";
    echo "<td>" . $row['low'] . "</td>";
    echo "<td>" . $row['closing'] . "</td>";
    echo "</tr>";
}
echo "</table>";

mysql_close();
?>