<?php
# index.php?year=2023&month=12


if (!isset($_GET['year'])) {
    $year = date("Y");
}
if (!isset($_GET['month'])) {
    $month = date("m");
}

$year = isset($_GET['year']) ? $_GET['year'] : date('Y');
$month = isset($_GET['month']) ? $_GET['month'] : date('m');
$daysInMonth = date('t', mktime(0, 0, 0, $month, 1, $year));
$monthName = date('F', mktime(0, 0, 0, $month, 10));
$backgroundImage = $year . '/' . $month . '_' . $monthName . '.jpg';

$dt1 = strtotime($year .'-'. $month .'-'. '01');
$prev_month_int = strtotime("-1 month", $dt1);
$prev_month = gmdate("m", $prev_month_int);

$prev_year_int = strtotime("-1 month", $dt1);
$prev_year = gmdate("Y", $prev_year_int);

$next_month_int = strtotime("+1 month", $dt1);
$next_month = gmdate("m", $next_month_int);

$next_year_int = strtotime("+1 month", $dt1);
$next_year = gmdate("Y", $next_year_int);


echo "<!DOCTYPE html><html><head><title>$monthName - $year (Calendar)</title>";
echo "<style>
        body { color:white;width: 100%;
    margin: auto;}
        #calendar {

    position: relative;
    bottom: 173px;
    right: -605px;
    width: 500px;
    height: 98px;
    color: #ffca00;
    background-color: black;
}
        body { background-color: black;  background-size: cover;font-family: monospace}
        caption { color: #ffca00;
    height: 23px;
    font-size: 20px;
    background: linear-gradient(to left, #999 10%, #242424 50%, #999 80%); }
        h1 { font-family: 'Times New Roman';}
        td{text-align: center; width: 10px !important;}
        img {height: 700px;clip-path: polygon(5% 5%, 91% 0%, 100% 105%, 75% 87%, 75% 500%, 50% 750%, 10% 75%);padding: 1rem;color: white;
    border-width: 109px;
    border-style: solid;
    border-image: linear-gradient( to bottom, red, rgba(0, 0, 0, 0) ) 1 100%;}
    h2 {color: red;}
    .gallery {
position: relative;
    top: -47px;
}
.titl {
    color: #bbbbbb;
    font-size: 60px;
    top: 7px;
    left: 132px;
    font-family: times new roman;
    background: -webkit-linear-gradient(#d7d7d7, #080808);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent; }
.nextones a {
color: white;
}
      </style>";
echo "</head>";
echo "<div class='nextones'><a href='/'>Home </a> | <a href='index.php?year=$prev_year&month=$prev_month'>Previous month </a> | <a href='index.php?year=$next_year&month=$next_month'> Next month</a></div>";
echo "<body>";
echo "<div class='titl'>$monthName $year</div>";
echo "<div class='gallery'><img src='$backgroundImage' /> </div>";
echo "<table id='calendar'>";
echo "<caption>$monthName $year</caption>";
echo "<tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr>";

for ($i = 1; $i <= $daysInMonth; $i++) {
    $dayOfWeek = date('w', mktime(0, 0, 0, $month, $i, $year));
    if ($i == 1) {
        echo "<tr>";
        for ($j = 0; $j < $dayOfWeek; $j++) {
            echo "<td></td>";
        }
    } else if ($dayOfWeek == 0) {
        echo "</tr><tr>";
    }

    $today = $year == date('Y') && $month == date('m') && $i == date('j');
    echo $today ? "<td style='background-color:#494949;border-radius:50%;'>$i</td>" : "<td>$i</td>";

    if ($i == $daysInMonth) {
        echo "</tr>";
    }
}
echo "</table>\n";



echo "</body></html>";
?>

