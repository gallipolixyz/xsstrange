<?php

$query = isset($_GET['q']) ? $_GET['q'] : '';
$results = '';

if ($query) {
    $results = "<h3>Search Results:</h3>";
    $results .= "<p>Results for \"$query\":</p>";
    $results .= "<div class='search-results'>No results found.</div>";
}
?>

<!DOCTYPE html>
<html>
<body>
    <div class="search-container">
        <h2>PHP Search Engine</h2>
        <form method="GET" action="">
            <label for="q">Search Term:</label>
            <input type="text" id="q" name="q" placeholder="Enter a term to search..." value="<?php echo $query; ?>">
            <button type="submit">Search</button>
        </form>
        
        <div id="results">
            <?php echo $results; ?>
        </div>
    </div>
</body>
</html>
