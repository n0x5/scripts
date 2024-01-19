<title> TV Database</title>
<body style="width:600px;font-family:monospace;">
<h1> TV Database</h1>


<table>
<?php
$dir = 'sqlite:tv.db';
$dbh  = new PDO($dir, null, null) or die("cannot open the database");
$query = "select imdb_id, show_title, count(imdb_id) c, air_date, count(distinct(season_number)) from tv group by show_title having c > 0 order by show_title ";
//$result = $dbh->query("select * from dp_table");
//$result2 = $result->fetchAll();
//echo count($result2) . ' files parsed<br>';
foreach ($dbh->query($query) as $row) {
echo "<tr><th><img width='160px' src='cover_tv/" . $row[0] . ".jpg' /></th><th><b><a style='text-decoration: none;' href='episode.php?ep=$row[0]''>$row[1] ($row[3])</a> </b><hr>
$row[4] seasons, $row[2] episodes


</th></tr>";
}
?> 

</table>