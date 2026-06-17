<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

if (!isset($_FILES['file']) || $_FILES['file']['error'] !== UPLOAD_ERR_OK) {
    $code = $_FILES['file']['error'] ?? -1;
    http_response_code(400);
    echo json_encode(['error' => "File upload error (code $code)"]);
    exit;
}

$file = $_FILES['file'];
$ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
if (!in_array($ext, ['pdf', 'txt'], true)) {
    http_response_code(400);
    echo json_encode(['error' => 'Only PDF and TXT files are supported']);
    exit;
}

$backend_url = rtrim(getenv('BACKEND_URL') ?: 'http://localhost:8000', '/');

$ch = curl_init("$backend_url/api/upload");
$cfile = new CURLFile($file['tmp_name'], $file['type'] ?: 'application/octet-stream', $file['name']);

curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => ['file' => $cfile],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 120,
    CURLOPT_SSL_VERIFYPEER => false,
]);

$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curl_err  = curl_error($ch);
curl_close($ch);

if ($response === false) {
    http_response_code(502);
    echo json_encode(['error' => "Backend unreachable: $curl_err"]);
    exit;
}

http_response_code($http_code);
echo $response;
