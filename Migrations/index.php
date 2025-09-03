<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Registration</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f2f5;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
            text-align: center;
        }
        h1 {
            font-size: 1.5em;
            color: #333;
        }
        label {
            font-weight: bold;
            margin-top: 10px;
            display: block;
        }
        input[type="text"], input[type="email"], input[type="password"] {
            width: 100%;
            padding: 10px;
            margin-top: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 1em;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1em;
            margin-top: 15px;
        }
        button:hover {
            background-color: #45a049;
        }
        .error {
            color: red;
            margin-top: 10px;
        }
        .success {
            color: green;
            margin-top: 10px;
        }
        .activation-link {
            margin-top: 15px;
            font-size: 0.95em;
            word-wrap: break-word;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>User Registration</h1>
        
        <form method="POST" action="">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>

            <label for="email">Email Address:</label>
            <input type="email" id="email" name="email" required>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>

            <label for="re_password">Confirm Password:</label>
            <input type="password" id="re_password" name="re_password" required>

            <button type="submit" name="register">Register</button>
        </form>

        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            // Database config
            $servername = "localhost";
            $usernameDB = "root";
            $passwordDB = "ascent";
            $dbname = "tbot_base";

            // Connect to DB
            $conn = new mysqli($servername, $usernameDB, $passwordDB, $dbname);

            // Check connection
            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }

            $username = isset($_POST['username']) ? $conn->real_escape_string($_POST['username']) : '';
            $email = isset($_POST['email']) ? $conn->real_escape_string($_POST['email']) : '';
            $password = isset($_POST['password']) ? $_POST['password'] : '';
            $re_password = isset($_POST['re_password']) ? $_POST['re_password'] : '';
            $last_ip = $_SERVER['REMOTE_ADDR'];

            if ($password !== $re_password) {
                echo "<p class='error'>Passwords do not match.</p>";
            } else {
                // Hash password with Argon2i
                $hashed_password = password_hash($password, PASSWORD_ARGON2I);

                // Generate activation code
                $activation_code = bin2hex(random_bytes(16));

                // Insert new user
                $sql = "INSERT INTO users (username, password, email, last_ip, activation_code, activated) 
                        VALUES ('$username', '$hashed_password', '$email', '$last_ip', '$activation_code', 0)";

                if ($conn->query($sql) === TRUE) {
                    echo "<p class='success'>Registration successful. Please check your email to activate your account.</p>";

                    // Build activation link dynamically with current host
                    $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? "https://" : "http://";
                    $host = $_SERVER['HTTP_HOST'];
                    $activation_link = $protocol . $host . "/activate.php?code=$activation_code";

                    echo "<div class='activation-link'> 
                            <strong>Activation Link:</strong><br>
                            <a href='$activation_link'>$activation_link</a>
                          </div>";

                    // Send activation email
                    $subject = "Account Activation";
                    $message = "Hello, $username. To activate your account, please click the following link: $activation_link";
                    $headers = "From: admin@admin";

                    if (mail($email, $subject, $message, $headers)) {
                        echo "<p class='success'>An activation email has been sent.</p>";
                    } else {
                        echo "<p class='error'>Failed to send activation email.</p>";
                    }
                } else {
                    echo "<p class='error'>Error: " . $conn->error . "</p>";
                }
            }

            $conn->close();
        }
        ?>
    </div>
</body>
</html>
