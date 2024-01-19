<title> TV Database</title>
<body style="width:600px;font-family:monospace;">
<h1> TV Database</h1>


<table>
<?php
$episode = $_GET['ep'];
echo "<img width='300px' src='cover_tv/$episode.jpg' /><hr>";
$dir = 'sqlite:tv.db';
$dbh  = new PDO($dir, null, null) or die("cannot open the database");
$query = "select show_title, episode_title, air_date, episode_summary, season_number, episode_number, imdb_id from tv where imdb_id like '$episode' order by imdb_id, season_number ";

foreach ($dbh->query($query) as $row) {
echo "<div class='ep'><h2 style='display:inline;'>$row[4] | $row[5] </h2>-<h3 style='display:inline;'> $row[1] ($row[2])</h3><br>$row[3]<hr>";
}
?> 

</table>