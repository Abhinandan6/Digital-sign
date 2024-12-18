<!DOCTYPE html>
<html>

<head>
    <title>PDF Signer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }

        form {
            margin: 20px auto;
            width: 300px;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
        }

        input[type="file"] {
            margin-bottom: 10px;
        }

        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>

<body>
    <form action="sign_pdf.php" method="post" enctype="multipart/form-data">
        <label for="pdfFile">Select PDF to sign:</label>
        <input type="file" name="pdfFile" id="pdfFile">
        <br>
        <input type="submit" value="Sign PDF" name="submit">
    </form>
</body>

</html>

<?php
if (isset($_POST["submit"])) {
    $uploadDir = "uploads/";
    $uploadedPdfPath = $uploadDir . basename($_FILES["pdfFile"]["name"]);

    if (move_uploaded_file($_FILES["pdfFile"]["tmp_name"], $uploadedPdfPath)) {
        // Database connection
        $conn = new mysqli("localhost", "root", "", "loginsystem");
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        // Assuming the user ID is known or retrieved from session/other means
        $userId = 1; // Example user ID

        // Fetch user and key details
        $sql = "SELECT fname, lname, public_key, private_key FROM users u, pkey p WHERE u.id = ? and p.id = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ii", $userId, $userId);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($row = $result->fetch_assoc()) {
            $fname = $row["fname"];
            $lname = $row["lname"];
            $publicKey = $row["public_key"]; 
            $privateKey = $row["private_key"]; 

            // Create temporary files with more descriptive names
            $tempPublicKeyPath = tempnam(sys_get_temp_dir(), 'pub_key');
            $tempPrivateKeyPath = tempnam(sys_get_temp_dir(), 'priv_key');

            // Write key contents (ensure proper encoding)
            file_put_contents($tempPublicKeyPath, $publicKey);
            file_put_contents($tempPrivateKeyPath, $privateKey);

            // Command construction with proper argument escaping
            $escapedFname = escapeshellarg($fname);
            $escapedLname = escapeshellarg($lname);
            $escapedPublicKeyPath = escapeshellarg($tempPublicKeyPath);
            $escapedPrivateKeyPath = escapeshellarg($tempPrivateKeyPath);
            $escapedPdfPath = escapeshellarg($uploadedPdfPath);

            $command = "python sign2.py $escapedFname $escapedLname $escapedPublicKeyPath $escapedPrivateKeyPath $escapedPdfPath";
            $output = shell_exec($command);

            $signedPdfPath = $uploadDir . basename($uploadedPdfPath, '.pdf') . '_signed.pdf';
            if (copy($uploadedPdfPath, $signedPdfPath)) {
                echo "<p style='color: green;'>Signed PDF saved as $signedPdfPath</p>";
            } else {
                echo "<p style='color: red;'>Error saving signed PDF.</p>";
            }

            // Cleanup
            unlink($tempPublicKeyPath);
            unlink($tempPrivateKeyPath);

        } else {
            echo "<p style='color: red;'>User not found.</p>";
        }
        $conn->close();
    } else {
        echo "<p style='color: red;'>Error uploading file.</p>";
    }
}
?>

