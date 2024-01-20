<title>Second Sight wiki</title>
<body style="width:600px;font-family:monospace;">
<h1> Second Sight wiki</h1>


<?php
$category = $_GET['cat'];
$dir = 'sqlite:secondsight.db';
$dbh  = new PDO($dir, null, null) or die("cannot open the database");
$query = "select title, content from `secondsight` where content like '%$category%' order by title";
//$result = $dbh->query("select * from dp_table");
//$result2 = $result->fetchAll();
//echo count($result2) . ' files parsed<br>';
foreach ($dbh->query($query) as $row) {
echo "<a href='page.php?page=$row[0]'>$row[0]</a><br>";
} 
