<?php

$targetDir = "uploads/";

if (!file_exists($targetDir)) {
    mkdir($targetDir, 0755, true);
}

if (!empty($_FILES['file'])) {
    $tempFile = $_FILES['file']['tmp_name'];
    $fileName = $_FILES['file']['name'];
    $fileParts = pathinfo($fileName);

    $allowedTypes = array('jpg', 'jpeg', 'png', 'gif');

    if (in_array(strtolower($fileParts['extension']), $allowedTypes)) {
        $targetFile = $targetDir . $fileName;

        if (move_uploaded_file($tempFile, $targetFile)) {
            echo json_encode(["status" => "success", "message" => "File uploaded successfully."]);
        } else {
            http_response_code(500);
            echo json_encode(["status" => "error", "message" => "Error uploading file."]);
        }
    } else {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Invalid file type."]);
    }
} else {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "No file uploaded."]);
}
?>
