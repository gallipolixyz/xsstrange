<?php
// Basic Reflected XSS - PHP Search Form
// This demonstrates a reflected XSS vulnerability in PHP

$query = isset($_GET['q']) ? $_GET['q'] : '';
$results = '';

if ($query) {
    $results = "<h3>Arama Sonuçları:</h3>";
    $results .= "<p>\"$query\" için sonuçlar:</p>";
    $results .= "<div class='search-results'>Sonuç bulunamadı.</div>";
}
?>

<!DOCTYPE html>
<html>
<body>
    <div class="search-container">
        <h2>PHP Arama Motoru</h2>
        <form method="GET" action="">
            <label for="q">Arama Terimi:</label>
            <input type="text" id="q" name="q" placeholder="Arama yapmak için bir terim girin..." value="<?php echo $query; ?>">
            <button type="submit">Ara</button>
        </form>
        
        <div id="results">
            <?php echo $results; ?>
        </div>
    </div>
</body>
</html>
