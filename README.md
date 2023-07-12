# Gabe's Spreadsheet Processor

Gabe's Spreadsheet Processor, a Python application for processing spreadsheet files. It provides a user-friendly interface to browse and select spreadsheet files, preview data, and process files by removing specified columns.

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

Video guide(click image below)[slightly outdated]:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=qC1W0BDccj4
" target="_blank"><img src="http://img.youtube.com/vi/qC1W0BDccj4/0.jpg" width="240" height="180" border="10" /></a>

## TODO
- [x] Add support for more file types
- [x] Add uspport for different enocodings
- [ ] Allow the user to specify different columns to remove for each file
- [ ] Improve the GUI layout and design
  - [x] Add way to preview data
- [ ] Squash bugs
  - [x] Invalid Column Name
  - [x] Invalid File Type
- [ ] Add function for columns to keep
- [ ] Look into PyQt


The desktop icon was made by OkapiIsTired from https://www.favicon.cc/

Color Scheme used is Tokyo Night Light from https://github.com/enkia/tokyo-night-vscode-theme
