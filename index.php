<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gabe's Spreadsheet Processor</title>
    <script src="https://unpkg.com/htmx.org@1.9.8"></script>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>Gabe's Spreadsheet Processor</h1>
        <form id="fileForm" hx-post="process_files.php" hx-target="#preview" hx-encoding="multipart/form-data">
            <div class="file-upload">
                <label for="files">Select Files:</label>
                <input type="file" id="files" name="files[]" multiple>
            </div>
            <div class="column-input">
                <label for="columns">Columns to Remove (comma-separated):</label>
                <input type="text" id="columns" name="columns">
            </div>
            <button type="submit">Process Files</button>
        </form>
        <div id="preview"></div>
    </div>
</body>
</html>
