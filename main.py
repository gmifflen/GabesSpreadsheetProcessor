import pandas as pd
from pandas.errors import EmptyDataError, ParserError
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QGridLayout, QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
import os
import chardet


class Application(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # holds selected files names
        self.preview_rows_entry = None
        self.preview_rows_label = None
        self.preview_button = None
        self.process_button = None
        self.columns_entry = None
        self.columns_label = None
        self.filename_label = None
        self.browse_button = None
        self.filenames = []
        self.preview_windows = []

        # Set the background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor('#d5d6db'))
        self.setPalette(p)

        # Create UI elements
        self.create_widgets()

        # Set the window title
        self.setWindowTitle("Gabe's Spreadsheet Processor")

    def create_widgets(self):
        # Create a grid layout
        layout = QGridLayout(self)

        # Button for browsing and selecting Excel files
        self.browse_button = QPushButton("Browse Files")
        self.browse_button.setStyleSheet('background-color: #8be9fd')
        self.browse_button.clicked.connect(self.load_files)
        layout.addWidget(self.browse_button, 0, 0)

        # Label for showing selected file names
        self.filename_label = QLabel("No files selected")
        self.filename_label.setStyleSheet('color: #0f0f14')
        self.filename_label.setFont(QFont('Helvetica', 9, italic=True))
        layout.addWidget(self.filename_label, 0, 1)

        # Label for input field for column names to remove
        self.columns_label = QLabel("Columns to remove (comma-separated)")
        self.columns_label.setStyleSheet('color: #343b58')
        self.columns_label.setFont(QFont('Helvetica', 10))
        layout.addWidget(self.columns_label, 1, 0)

        # Entry widget for column names input
        self.columns_entry = QLineEdit()
        layout.addWidget(self.columns_entry, 2, 0, 1, 2)

        # Button for processing files
        self.process_button = QPushButton("Process Files")
        self.process_button.setStyleSheet('background-color: #50fa7b')
        self.process_button.clicked.connect(self.process_files)
        layout.addWidget(self.process_button, 3, 0, 1, 2)

        # Button to preview data
        self.preview_button = QPushButton("Preview Data")
        self.preview_button.setStyleSheet('background-color: #ff9e64')
        self.preview_button.clicked.connect(self.preview_data)
        layout.addWidget(self.preview_button, 4, 0, 1, 2)

        # Label for # of preview rows
        self.preview_rows_label = QLabel("Number of rows to preview:")
        self.preview_rows_label.setStyleSheet('color: #343b58')
        self.preview_rows_label.setFont(QFont('Helvetica', 10))
        layout.addWidget(self.preview_rows_label, 5, 0)

        # Entry for # of preview rows
        self.preview_rows_entry = QLineEdit()
        self.preview_rows_entry.setText('12')
        layout.addWidget(self.preview_rows_entry, 5, 1)

    def load_files(self):
        # Open a file dialog and get the selected filenames
        self.filenames, _ = QFileDialog.getOpenFileNames(self, "Select Files",
                                                         "",
                                                         "Spreadsheet files (*.xlsx *.csv *.ods);;All files (*)")
        if self.filenames:
            # Update the filename label text with selected files
            self.filename_label.setText(', '.join(self.filenames))

    def preview_data(self):
        # Check if any file is selected, else error message
        if not self.filenames:
            QMessageBox.critical(self, "Error", "No files selected")
            return

        # To only preview the 1st file
        filename = self.filenames[0]

        # Try to read file based on its extension
        try:
            data = self.read_file(filename)
        except (EmptyDataError, ParserError, FileNotFoundError) as e:
            QMessageBox.critical(self, "Error", f"Failed to read file {filename}. Make sure it's a valid spreadsheet file.")
            return

        # Get the number of rows to preview from the Entry widget
        try:
            num_rows = int(self.preview_rows_entry.text())
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid number of rows to preview.")
            return

        # Create a new window to display the data
        preview_window = QtWidgets.QWidget()
        preview_window.setWindowTitle(f"Data Preview - {os.path.basename(filename)}")
        table = QTableWidget()
        table.setRowCount(num_rows)
        table.setColumnCount(len(data.columns))
        table.setHorizontalHeaderLabels(data.columns)

        for row in range(num_rows):
            for col in range(len(data.columns)):
                table.setItem(row, col, QTableWidgetItem(str(data.iloc[row, col])))

        preview_layout = QtWidgets.QVBoxLayout()
        preview_layout.addWidget(table)
        preview_window.setLayout(preview_layout)
        preview_window.show()

        # Store the window to prevent it from being garbage collected
        self.preview_windows.append(preview_window)

    def process_files(self):
        # Show error and return if no files selected
        if not self.filenames:
            QMessageBox.critical(self, "Error", "No files selected")
            return

        # Get columns to remove from the Entry widget
        columns_to_remove = self.columns_entry.text().split(',')
        # Show error and return if no columns specified
        if not columns_to_remove:
            QMessageBox.critical(self, "Error", "No columns specified")
            return

        # Iterate over the selected files
        for filename in self.filenames:
            # Try and read the file, else error
            try:
                data = self.read_file(filename)
            except (EmptyDataError, ParserError, FileNotFoundError) as e:
                QMessageBox.critical(self, "Error", f"Failed to read file {filename}. Make sure it's a valid spreadsheet file.")
                return

            # Check if unwanted cols exist, else error
            missing_cols = [col for col in columns_to_remove if col not in data.columns]
            if missing_cols:
                QMessageBox.critical(self, "Error", f"The column(s) {', '.join(missing_cols)} do not exist in file {filename}.")
                return

            # drop unwanted cols
            data = data.drop(columns=columns_to_remove)

            # Save the data to a new file with "_cleaned" appended to the original filename
            base_filename, ext = os.path.splitext(filename)
            output_filename = f"{base_filename}_cleaned{ext}"

            if filename.endswith('.csv'):
                data.to_csv(output_filename, index=False)
            else:
                data.to_excel(output_filename, index=False)

        # Show success message when all files are processed
        QMessageBox.information(self, "Success", f"Files processed successfully")

    @staticmethod
    def detect_and_read_csv(filename):
        # Detects the encoding of a CSV file and read it
        with open(filename, 'rb') as f:
            result = chardet.detect(f.read())

        return pd.read_csv(filename, encoding=result['encoding'])

    @staticmethod
    def read_file(filename):
        if filename.endswith('.csv'):
            return Application.detect_and_read_csv(filename)
        elif filename.endswith(('.xlsx', '.ods')):
            return pd.read_excel(filename)
        else:
            raise Exception("Unsupported file type.")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    application = Application()
    application.show()

    sys.exit(app.exec_())
