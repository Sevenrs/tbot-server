<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro de Usuario</title>
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
    </style>
</head>
<body>
    <div class="container">
        <h1>Registro de Usuario</h1>
        
        <form method="POST" action="">
            <label for="username">Nombre de Usuario:</label>
            <input type="text" id="username" name="username" required>

            <label for="email">Correo Electrónico:</label>
            <input type="email" id="email" name="email" required>

            <label for="password">Contraseña:</label>
            <input type="password" id="password" name="password" required>

            <label for="re_password">Confirmar Contraseña:</label>
            <input type="password" id="re_password" name="re_password" required>

            <button type="submit" name="register">Registrar</button>
        </form>

        <?php
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            // Configuración de la base de datos
            $servername = "localhost";
            $usernameDB = "root";  // Cambia a tu usuario de MySQL
            $passwordDB = "ascent";      // Cambia a tu contraseña de MySQL
            $dbname = "tbot-game-local";

            // Conectar a la base de datos
            $conn = new mysqli($servername, $usernameDB, $passwordDB, $dbname);

            // Verificar la conexión
            if ($conn->connect_error) {
                die("Error de conexión: " . $conn->connect_error);
            }

            // Verificar si los campos existen en $_POST antes de acceder a ellos
            $username = isset($_POST['username']) ? $conn->real_escape_string($_POST['username']) : '';
            $email = isset($_POST['email']) ? $conn->real_escape_string($_POST['email']) : '';
            $password = isset($_POST['password']) ? $_POST['password'] : '';
            $re_password = isset($_POST['re_password']) ? $_POST['re_password'] : '';
            $last_ip = $_SERVER['REMOTE_ADDR'];

            // Verificar si las contraseñas coinciden
            if ($password !== $re_password) {
                echo "<p class='error'>Las contraseñas no coinciden.</p>";
            } else {
                // Hash de la contraseña usando Argon2i
                $hashed_password = password_hash($password, PASSWORD_ARGON2I);

                // Generar un código único de activación
                $activation_code = bin2hex(random_bytes(16)); // 32 caracteres hexadecimales

                // Preparar la consulta de inserción
                $sql = "INSERT INTO users (username, password, email, last_ip, activation_code, activated) 
                        VALUES ('$username', '$hashed_password', '$email', '$last_ip', '$activation_code', 0)";

                if ($conn->query($sql) === TRUE) {
                    echo "<p class='success'>Registro exitoso. Por favor, revisa tu correo electrónico para activar tu cuenta.</p>";

                    // Enviar el correo de activación
                    $activation_link = "http://127.0.0.1/activar.php?code=$activation_code";
                    $subject = "Activación de cuenta";
                    $message = "Hola, $username. Para activar tu cuenta, por favor haz clic en el siguiente enlace: $activation_link";
                    $headers = "From: admin@admin";

                    // Usar la función mail() de PHP para enviar el correo
                    if (mail($email, $subject, $message, $headers)) {
                        echo "<p class='success'>Se ha enviado un correo de activación.</p>";
                    } else {
                        echo "<p class='error'>Error al enviar el correo de activación.</p>";
                    }
                } else {
                    echo "<p class='error'>Error: " . $conn->error . "</p>";
                }
            }

            // Cerrar la conexión
            $conn->close();
        }
        ?>
    </div>
</body>
</html>
