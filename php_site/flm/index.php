<title> FLM Database</title>
<body style="width:600px;font-family:monospace;">
<h1> FLM Database</h1>


<table>
<?php
$dir = 'sqlite:movies_flm_new.db';
$dbh  = new PDO($dir, null, null) or die("cannot open the database");
$query = "select * from moviesflm order by year desc ";
//$result = $dbh->query("select * from dp_table");
//$result2 = $result->fetchAll();
//echo count($result2) . ' files parsed<br>';
foreach ($dbh->query($query) as $row) {
echo "<tr><th><img width='160px' src='covers_flm/" . $row[0] . ".jpg' /></th><th><b>$row[1] ($row[8])</b><hr>
<b>[ $row[11] ]</b> <br>
$row[9]<br>
$row[10]<br>
$row[5]<br>
$row[0]

</th></tr>";
}
?> 

</table>