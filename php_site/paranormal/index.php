<title>paranormal wiki</title>
<body style="width:600px;font-family:monospace;text-decoration: none;">
<h1>paranormal wiki</h1>


<?php

$dir = 'sqlite:paranormal.db';
$dbh  = new PDO($dir, null, null) or die("cannot open the database");
$query = "select subsection, section from paranormal order by section asc";
foreach ($dbh->query($query) as $row) {
echo "<a style='text-decoration: none;' href='page.php?cat=$row[0]'>$row[1] - $row[0]</a><br>";
}

