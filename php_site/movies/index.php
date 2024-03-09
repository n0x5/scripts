<title>Movie Database</title>
<body style="width:600px;font-family:monospace;">
<h1>Movie Database</h1>
<style>
table, th, td {
  border: 1px solid black;
}
</style>
<a href="?genre=action">Action</a> | <a href="?genre=adventure">Adventure</a> | <a href="?genre=animation">Animation</a> | <a href="?genre=comedy">Comedy</a> | <a href="?genre=crime">Crime</a> 
| <a href="?genre=documentary">Documentary</a> | <a href="?genre=drama">Drama</a> | <a href="?genre=family">Family</a> | <a href="?genre=history">History</a> | <a href="?genre=horror">Horror</a> 
| <a href="?genre=mystery">Mystery</a> | <a href="?genre=sci-fi">Sci-Fi</a> | <a href="?genre=sport">Sport</a> | <a href="?genre=thriller">Thriller</a> | <a href="?genre=war">War</a> | <a href="?genre=western">Western</a> | 
<hr>
<table>
<?php
$genre = $_GET['genre'];
$dir = 'sqlite:movies.db';
$dbh  = new PDO($dir, null, null) or die("cannot open the database");
$query = "select movies.release, movies.director, movies.imdb, movies.infogenres, movies.year, boxoffice.rlid, boxoffice.wide_theatersopen 
from movies join boxoffice on movies.imdb = boxoffice.imdbid where cast(replace(wide_theatersopen, ',', '') as int) > 2000 and boxoffice.wide_theatersopen != 'None' and infogenres like '%$genre%' group by movies.imdb order by movies.year desc";

foreach ($dbh->query($query) as $row) {
echo "<tr><th><img width='160px' src='covers/" . $row[2] . ".jpg' /></th><th><b>$row[0] ($row[4])</b>

<hr>
$row[3] <br>
$row[6]
</th></tr>";
}
?> 

</table>