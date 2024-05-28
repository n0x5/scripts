
<body style="width:600px;font-family:monospace;text-decoration: none;">



<?php
$cat = $_GET['cat'];
$dir = 'sqlite:paranormal.db';
$dbh  = new PDO($dir, null, null) or die("cannot open the database");
$query = "select subsection, section, body from paranormal where subsection like '$cat'";

foreach ($dbh->query($query) as $row) {
echo "<h2>$row[1] - $row[0]</h2><hr>";
echo "<pre> $row[2] </pre>";
}