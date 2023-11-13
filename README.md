# Gabe's Spreadsheet Processor

Gabe's Spreadsheet Processor is a PHP application for processing spreadsheet files. It provides a user-friendly interface to browse and select spreadsheet files, preview data, and process files by removing specified columns.

![alt text](https://github.com/gmifflen/GabesSpreadsheetProcessor/blob/main/sc.png?raw=true)

## Key Features
- Browse and select multiple spreadsheet files (supported file types: .xlsx, .csv, .ods)
- Preview data from the selected files
- Specify columns to remove from the files
- Process the selected files by removing the specified columns
- Save processed data to new files with "_cleaned" appended to the original filenames

## Usage

1. Click the "Browse Files" button to select one or more spreadsheet files.
2. The selected filenames will be displayed in the interface.
3. To preview data from the first selected file, click the "Preview Data" button.
4. Enter the column names (comma-separated) that you want to remove from the files in the "Columns to remove" field.
5. Click the "Process Files" button to remove the specified columns from the selected files.
6. Processed files will be saved with "_cleaned" appended to their original filenames.
7. A success message will be displayed when all files are processed.

Note: The application supports Excel (.xlsx), CSV (.csv), and OpenDocument Spreadsheet (.ods) file formats. The encoding detection feature ensures accurate reading of CSV files.

## Installation and Requirements

This application requires PHP 8.2.4 and HTMX to run. You can install PHP and HTMX as follows:

- [PHP Installation](https://www.php.net/manual/en/install.php)
- [HTMX Installation](https://htmx.org/install/)

## Video Guide (For the Python version, but it's still the same thing)

[![Watch the video guide](http://img.youtube.com/vi/qC1W0BDccj4/0.jpg)](http://www.youtube.com/watch?feature=player_embedded&v=qC1W0BDccj4)

## TODO
- [x] Add support for more file types
- [x] Add support for different encodings
- [ ] Allow the user to specify different columns to remove for each file
- [ ] Improve the GUI layout and design
  - [] Add a way to preview data
  - [x] Look into using HTMX for the GUI
- [ ] Squash bugs
  - [x] Invalid Column Name
  - [x] Invalid File Type
- [ ] Add a function for columns to keep
- [ ] Add a progress bar
