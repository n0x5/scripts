<html>
<body style='font-family:monospace'>



<?php
$path = (isset($_GET['path'])) ? htmlentities($_GET['path']) : '.'; 
$real_path = realpath($path);
$thumbMaxSize = 200;
$loc_file = basename($_SERVER["SCRIPT_NAME"]);
echo "<a href='/$loc_file'>Home</a>";
echo "<title>$path</title>";
echo "<h1>$path Gallery</h1>";


if (strpos($real_path, dirname(__DIR__)) !== 0) {
    die('Invalid path');
}
$files = scandir($real_path);

foreach($files as $file) {
    if($file === "." || $file === ".." || $file === "thumbs" || $file === "OneDrive_Folder_Icon.png") continue;
    $full_path = "$real_path/$file";
    if (is_dir($full_path)) {
        $url = '?path=' . urlencode("$path/$file");
        echo "<div style='width:150px;float: left;margin: 10px;'><a href='$url'>
                <img src=OneDrive_Folder_Icon.png /><div style='position: relative;top: -50px;color: black;font-weight: 900;font-size: 15px;text-align: center;' class='foldername'>$file</div></a></div></a></div>";
    } elseif (is_readable($full_path)) {
        
        $thumbsfolder = $real_path . '/thumbs/';
        $thumbPath = $thumbsfolder . basename($full_path);
        if (!is_dir($thumbsfolder)) {
            mkdir($thumbsfolder);
        }
        if (!file_exists($thumbPath)) {
            $thumbnail = create_thumbnail($full_path, $thumbPath, $thumbMaxSize);
        }
        list($width, $height) = getimagesize("$full_path");
        list($width_thumb, $height_thumb) = getimagesize("$thumbPath");
        echo "<div class='img' style='width:$width_thumb;float:left;margin: 5px;'><a href=$path/$file><img src=$path/thumbs/$file /></a><div style='text-align:center;font-size:11px;line-height: 90%;'> $width x $height <br>-<br>$file</div></div>\n";
    } else {
        continue;
    }
}


function create_thumbnail($originalImage, $thumbnailImage, $thumbMaxSize){
    list($origWidth, $origHeight) = getimagesize($originalImage);
    $thumbRatio = $thumbMaxSize / max($origWidth, $origHeight);
    $thumbWidth = intval($origWidth * $thumbRatio);
    $thumbHeight = intval($origHeight * $thumbRatio);

    if ($origWidth > $origHeight) {
        $new_height = $thumbMaxSize;
        $new_width = intval($origWidth*($new_height/$origHeight));
    } else {
        $new_width = $thumbMaxSize;
        $new_height = intval($origHeight*($new_width/$origWidth));
    }
    if (str_contains($originalImage, '.jpg')) {
        $thumbImg = imagecreatetruecolor($new_width, $new_height);
        $srcImg = imagecreatefromjpeg($originalImage);

        imagecopyresampled($thumbImg, $srcImg, 0, 0, 0, 0, $new_width, $new_height, $origWidth, $origHeight);
        imagejpeg($thumbImg, $thumbnailImage);
        imagedestroy($srcImg);
        imagedestroy($thumbImg);
    }
    return true;
}
?>

</body>
</html>