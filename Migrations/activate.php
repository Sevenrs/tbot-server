<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Activation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f6f9;
        }
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            max-width: 450px;
            width: 100%;
            text-align: center;
        }
        h1 {
            font-size: 1.8em;
            color: #333;
            margin-bottom: 15px;
        }
        label {
            display: block;
            font-size: 0.95em;
            color: #555;
            margin-bottom: 20px;
            word-wrap: break-word;
        }
        .success, .error {
            font-size: 1.2em;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Account Activation</h1>

    <label>
        Example activation link:<br>
        <?php
        $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? "https://" : "http://";
        $host = $_SERVER['HTTP_HOST'];
        echo $protocol . $host . "/activate.php?code=yourcode";
        ?>
    </label>

    <?php
    // Connect to the database
    $servername = "localhost";
    $usernameDB = "root";  
    $passwordDB = "ascent";     
    $dbname = "tbot_base";
    $conn = new mysqli($servername, $usernameDB, $passwordDB, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection error: " . $conn->connect_error);
    }

    if (isset($_GET['code'])) {
        $activation_code = $conn->real_escape_string($_GET['code']);
        
        // Verify if the activation code exists in the database and the email is not yet verified
        $sql = "SELECT * FROM users WHERE activation_code = '$activation_code' AND email_verified = 0";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            // User found, proceed with activation
            $sql_update = "UPDATE users SET email_verified = 1, activation_code = NULL WHERE activation_code = '$activation_code'";

            if ($conn->query($sql_update) === TRUE) {
                echo "<p class='success'>Your account has been successfully activated. You can now log in.</p>";
            } else {
                echo "<p class='error'>Error activating the account. Please try again later.</p>";
            }
        } else {
            echo "<p class='error'>Invalid or already used activation code.</p>";
        }
    } else {
        echo "<p class='error'>No valid activation code was provided.</p>";
    }

    $conn->close();
    ?>
</div>

</body>
</html>
