<?php
$host = "localhost";
$user = "root";
$pass = "";
$dbname = "wastemap";

// Connexion à la base de données
$conn = new mysqli($host, $user, $pass, $dbname);

// Vérifier la connexion
if ($conn->connect_error) {
    die("Échec de la connexion : " . $conn->connect_error);
}

// Récupérer les données du formulaire
$nom = $_POST['nom'];
$latitude = $_POST['latitude'];
$longitude = $_POST['longitude'];
$type_dechet = $_POST['type_dechet'];
$description = $_POST['description'] ?? '';

// Gérer le fichier image
$photo_path = '';
if (isset($_FILES['photo']) && $_FILES['photo']['error'] === 0) {
    $uploads_dir = 'uploads/';
    if (!is_dir($uploads_dir)) {
        mkdir($uploads_dir, 0755, true);
    }

    $photo_name = basename($_FILES['photo']['name']);
    $target_path = $uploads_dir . time() . '_' . $photo_name;

    if (move_uploaded_file($_FILES['photo']['tmp_name'], $target_path)) {
        $photo_path = $target_path;
    } else {
        die("Erreur lors du téléchargement de l'image.");
    }
}

// Insérer dans la base
$sql = "INSERT INTO signalements (nom, latitude, longitude, type_dechet, photo, description)
        VALUES (?, ?, ?, ?, ?, ?)";

$stmt = $conn->prepare($sql);
$stmt->bind_param("sddsss", $nom, $latitude, $longitude, $type_dechet, $photo_path, $description);

if ($stmt->execute()) {
    echo "✅ Signalement enregistré avec succès !";
} else {
    echo "❌ Erreur : " . $stmt->error;
}

$stmt->close();
$conn->close();
?>
