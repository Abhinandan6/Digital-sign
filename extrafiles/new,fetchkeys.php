<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "loginsystem";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch keys
$sql = "SELECT private_key, public_key FROM pkey WHERE id = 1"; // Adjust the ID as needed
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    echo json_encode(['private_key' => $row['private_key'], 'public_key' => $row['public_key']]);
} else {
    echo json_encode(['error' => 'No keys found.']);
}

$conn->close();
?>