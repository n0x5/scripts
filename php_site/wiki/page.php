
<body style="width:600px;font-family:monospace;">



<?php
$page = $_GET['page'];
$dir = 'sqlite:secondsight.db';
$dbh  = new PDO($dir, null, null) or die("cannot open the database");
$query = "select title, content from `secondsight` where title like '%$page%' order by title";
//$result = $dbh->query("select * from dp_table");
//$result2 = $result->fetchAll();
//echo count($result2) . ' files parsed<br>';
foreach ($dbh->query($query) as $row) {
$cont2 = preg_replace('/\[\[File:(.+?)\|/i', '<img src="secondsight_images/$1" />', $row[1]);
$cont22 = preg_replace('/\=\=(.+?)\=\=/i', '<h4 style="display:inline;">$1</h4>', $cont2);
$cont222 = preg_replace('/\[\[(.+?)\]\]/i', '<a href="page.php?page=$1">$1</a>', $cont22);
echo "<title>$row[0]</title><h2>$row[0]</h2><hr><pre style='max-width:900px;white-space: pre-wrap;word-wrap: break-word;'>$cont222</pre>";
} 
 
