Sure, here's a simple README.md for your application:

---

# Gabe's XLSX Processor

This application provides a simple graphical user interface for editing spreadsheet files. It allows you to remove specific columns from one or multiple files at once.

![alt text](https://github.com/gmifflen/GabesSpreadsheetProcessor/blob/main/sc.png?raw=true)

## Usage

1. Click the "Browse Excel Files" button to select one or multiple spreadsheet files that you want to clean. The application supports Excel (.xlsx and .xls) files.

2. Enter the names of the columns you want to remove in the text field, separated by commas.

3. Click the "Process Files" button. The application will read each file, remove the specified columns, and write the cleaned data to a new file with "_cleaned" appended to the original filename.

Video guide(click image below):

<a href="http://www.youtube.com/watch?feature=player_embedded&v=qC1W0BDccj4
" target="_blank"><img src="http://img.youtube.com/vi/qC1W0BDccj4/0.jpg" width="240" height="180" border="10" /></a>

## TODO
- Add support for more file types
- Allow the user to specify different columns to remove for each file
- Improve the GUI layout and design
- Squash bugs
  - Invalid Column Name
  - Invalid File Type


The desktop icon was made by OkapiIsTired from https://www.favicon.cc/

Color Scheme used is Tokyo Night Light from https://github.com/enkia/tokyo-night-vscode-theme
