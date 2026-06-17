<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);
header('Content-Type: application/json');
echo json_encode([
    'curl_loaded' => extension_loaded('curl'),
    'php_version' => PHP_VERSION,
    'backend_url'  => getenv('BACKEND_URL') ?: '(not set)',
    'upload_max'   => ini_get('upload_max_filesize'),
]);
