<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Activación de Cuenta</title>
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
            max-width: 400px;
            width: 100%;
            text-align: center;
        }
        h1 {
            font-size: 1.8em;
            color: #333;
            margin-bottom: 20px;
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
    <h1>Activación de Cuenta</h1>

    <?php
    // Conectar a la base de datos
    $servername = "localhost";
    $usernameDB = "root";  
    $passwordDB = "ascent";     
    $dbname = "tbot-game-local";
    $conn = new mysqli($servername, $usernameDB, $passwordDB, $dbname);

    // Verificar la conexión
    if ($conn->connect_error) {
        die("Error de conexión: " . $conn->connect_error);
    }

    if (isset($_GET['code'])) {
        $activation_code = $conn->real_escape_string($_GET['code']);
        
        // Verificar si el código de activación existe en la base de datos y si el correo no está verificado
        $sql = "SELECT * FROM users WHERE activation_code = '$activation_code' AND email_verified = 0";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            // Usuario encontrado, proceder con la activación
            $sql_update = "UPDATE users SET email_verified = 1, activation_code = NULL WHERE activation_code = '$activation_code'";

            if ($conn->query($sql_update) === TRUE) {
                echo "<p class='success'>Tu cuenta ha sido activada exitosamente. Ahora puedes iniciar sesión.</p>";
            } else {
                echo "<p class='error'>Error al activar la cuenta. Intenta nuevamente más tarde.</p>";
            }
        } else {
            echo "<p class='error'>Código de activación inválido o ya utilizado.</p>";
        }
    } else {
        echo "<p class='error'>No se ha proporcionado un código de activación válido.</p>";
    }

    $conn->close();
    ?>
</div>

</body>
</html>
