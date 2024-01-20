<title>Second Sight wiki</title>
<body style="width:600px;font-family:monospace;">
<h1>Second Sight wiki</h1>


<?php
$dir = 'sqlite:secondsight.db';
$dbh  = new PDO($dir, null, null) or die("cannot open the database");
$query = "select title from `secondsight` where title like '%Category%' order by title";
foreach ($dbh->query($query) as $row) {
echo "<a href='category.php?cat=$row[0]'>$row[0]</a><br>";
}