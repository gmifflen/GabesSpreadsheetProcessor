<?php
require_once 'SimpleXLSX.php';
require_once 'SimpleXLSXGen.php';

// read CSV files
function readCSV($filename): array
{
    $data = [];
    if (($handle = fopen($filename, "r")) !== FALSE) {
        while (($row = fgetcsv($handle, 1000, ",")) !== FALSE) {
            $data[] = $row;
        }
        fclose($handle);
    }
    return $data;
}

// write CSV files
function writeCSV($filename, $data): void
{
    $file = fopen($filename, 'w');
    foreach ($data as $row) {
        fputcsv($file, $row);
    }
    fclose($file);
}

// read XLSX files using SimpleXLSX
function readXLSX($filename): false|array
{
    if ($xlsx = SimpleXLSX::parse($filename)) {
        return $xlsx->rows();
    }
    return false;
}

// write XLSX files using SimpleXLSXGen
function writeXLSX($filename, $data): void
{
    $xlsx = SimpleXLSXGen::fromArray($data);
    $xlsx->saveAs($filename);
}

// remove specified columns
function removeColumns($data, $columnsToRemove) {
    foreach ($data as &$row) {
        foreach ($columnsToRemove as $col) {
            $index = array_search($col, $row);
            if ($index !== false) {
                unset($row[$index]);
            }
        }
        $row = array_values($row); // re-index array
    }
    return $data;
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (empty($_FILES['files']['name'][0])) {
        exit('No files selected.');
    }

    $files = $_FILES['files'];
    $columnsToRemove = array_map('trim', explode(',', $_POST['columns']));
    $processedFiles = [];

    foreach ($files['tmp_name'] as $index => $tmpName) {
        $filename = $files['name'][$index];
        $ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));

        // read file based on extension
        $data = $ext === 'csv' ? readCSV($tmpName) : readXLSX($tmpName);
        if (!$data) {
            echo "Failed to read file: $filename<br>";
            continue;
        }

        $processedData = removeColumns($data, $columnsToRemove);
        $savePath = 'uploads/' . basename($filename, ".$ext") . '_processed.' . $ext;

        // write file based on extension
        if ($ext === 'csv') {
            writeCSV($savePath, $processedData);
        } elseif ($ext === 'xlsx') {
            writeXLSX($savePath, $processedData);
        } else {
            echo "Unsupported file format: $filename<br>";
            continue;
        }

        $processedFiles[] = $savePath;
    }

    // generate download links for processed files
    foreach ($processedFiles as $file) {
        echo "<a href='$file' download>" . basename($file) . "</a><br>";
    }
}
?>
