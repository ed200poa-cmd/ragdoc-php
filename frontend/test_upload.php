<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);
header('Content-Type: application/json');

$info = [
    'method'     => $_SERVER['REQUEST_METHOD'],
    'files'      => isset($_FILES['file']) ? [
        'name'  => $_FILES['file']['name'],
        'size'  => $_FILES['file']['size'],
        'error' => $_FILES['file']['error'],
        'tmp'   => $_FILES['file']['tmp_name'],
        'tmp_exists' => file_exists($_FILES['file']['tmp_name']),
    ] : 'NOT SET',
    'backend_url' => getenv('BACKEND_URL') ?: 'NOT SET',
];

if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
    // Try forwarding to backend
    $backend_url = rtrim(getenv('BACKEND_URL') ?: 'http://localhost:8000', '/');
    $ch = curl_init("$backend_url/api/upload");
    $cfile = new CURLFile(
        $_FILES['file']['tmp_name'],
        $_FILES['file']['type'] ?: 'text/plain',
        $_FILES['file']['name']
    );
    curl_setopt_array($ch, [
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => ['file' => $cfile],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 30,
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_VERBOSE        => false,
    ]);
    $res = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err  = curl_error($ch);
    curl_close($ch);
    $info['backend_status'] = $code;
    $info['backend_response'] = $res ?: "CURL ERROR: $err";
}

echo json_encode($info, JSON_PRETTY_PRINT);
