import pandas as pd
from pandas.errors import EmptyDataError
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from pandastable import Table


# main application
class Application(tk.Frame):
    # Initialize the Application class
    def __init__(self, master=None):
        super().__init__(master)

        # holds selected files names
        self.preview_button = None
        self.filenames = None

        # UI element
        self.process_button = None
        self.columns_entry = None
        self.columns_label = None
        self.browse_button = None
        self.filename_label = None

        # Assign the master (root window)
        self.master = master

        # Set the window title
        self.master.title("Gabe's Spreadsheet Processor")

        # TODO figure out a way to not use this or the below one if possible
        # Should set background, but it's more like a border than bg; not great, but works.
        self.master.configure(bg='#d5d6db')

        # Actually sets the bg, but not the border which has to be set above, changed to a grey to show problem
        self.configure(bg='#282828')

        # Arrange this frame widget in a grid layout with padding
        self.grid(padx=10, pady=10)

        # Create UI elements
        self.create_widgets()

    # Method to create and configure widgets
    def create_widgets(self):
        # Label for showing selected file names
        self.filename_label = tk.Label(self, text="No files selected", font=('Helvetica', 9, 'italic'), fg='#0f0f14',
                                       bg='#d5d6db')
        self.filename_label.grid(row=0, column=1, sticky='w')

        # Button for browsing and selecting Excel files
        self.browse_button = tk.Button(self, text="Browse Files", command=self.load_files, bg='#8be9fd',
                                       width=20)
        self.browse_button.grid(row=0, column=0, pady=(0, 10))

        # Label for input field (Entry widget) for column names to remove
        self.columns_label = tk.Label(self, text="Columns to remove (comma-separated)", font=('Helvetica', 10),
                                      fg='#343b58', bg='#d5d6db')
        self.columns_label.grid(row=1, column=0, sticky='w')

        # Entry widget for column names input
        self.columns_entry = tk.Entry(self, width=40)
        self.columns_entry.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        # Button for processing files
        self.process_button = tk.Button(self, text="Process Files", command=self.process_files, bg='#50fa7b',
                                        width=20)
        self.process_button.grid(row=3, column=0, columnspan=2)

        # Button to preview data
        self.preview_button = tk.Button(self, text="Preview Data", command=self.preview_data, bg='lightyellow',
                                        width=20)
        self.preview_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    # Method to load files, triggered by "Browse Excel Files" button
    def load_files(self):
        # Open a file dialog and get the selected filenames
        self.filenames = filedialog.askopenfilenames(
            filetypes=(("Spreadsheet files", "*.xlsx *.csv *.ods"), ("All files", "*.*")))
        if self.filenames:
            # Update the filename label text with selected files
            self.filename_label['text'] = ', '.join(self.filenames)

    # Method ot preview
    def preview_data(self):
        if not self.filenames:
            messagebox.showerror("Error", "No files selected")
            return

        # To only preview the 1st file
        filename = self.filenames[0]

        try:
            if filename.endswith('.csv'):
                data = pd.read_csv(filename)
            else:
                data = pd.read_excel(filename)
                # pd.errors.EmptyDataError is meant for csv's when empty data or header is encountered
        except (pd.errors.EmptyDataError, FileNotFoundError) as e:
            # If the file couldn't be read, show an error message and end the function
            messagebox.showerror("Error", f"Failed to read file {filename}. Make sure it's a valid spreadsheet file.")
            return

        # Create a new window to display the data
        preview_window = tk.Toplevel(self.master)
        preview_window.title(f"Data Preview - {os.path.basename(filename)}")
        preview_frame = tk.Frame(preview_window)
        preview_frame.pack(fill='both', expand=True)
        table = Table(preview_frame, dataframe=data.head(5))
        table.show()

    # Method to process files, triggered by "Process Files" button
    def process_files(self):
        # Show error and return if no files selected
        if not self.filenames:
            messagebox.showerror("Error", "No files selected")
            return

        # Get columns to remove from the Entry widget
        columns_to_remove = self.columns_entry.get().split(',')
        # Show error and return if no columns specified
        if not columns_to_remove:
            messagebox.showerror("Error", "No columns specified")
            return

        # Iterate over the selected files
        for filename in self.filenames:
            try:
                # Check if file is csv
                if filename.endswith('.csv'):
                    # Try to read the Excel or ODS file
                    data = pd.read_csv(filename)
                else:
                    # Try to read the Excel or ODS file
                    data = pd.read_excel(filename)
            except (FileNotFoundError, pd.errors.EmptyDataError) as e:
                # If the file couldn't be read, show an error message and end the function
                messagebox.showerror("Error",
                                     f"Failed to read file {filename}. Make sure it's a valid spreadsheet file.")
                return

            # Check if any of the columns specified to remove are not in the dataframe
            missing_cols = [col for col in columns_to_remove if col not in data.columns]
            # If there are any such columns, show an error message and end the function
            if missing_cols:
                messagebox.showerror("Error",
                                     f"The column(s) {', '.join(missing_cols)} do not exist in file {filename}")
                return

            # Remove the specified columns
            data = data.drop(columns=columns_to_remove)

            # Save the data to a new file with "_cleaned" appended to the original filename
            base_filename, ext = os.path.splitext(filename)
            output_filename = f"{base_filename}_cleaned{ext}"

            if filename.endswith('.csv'):
                data.to_csv(output_filename, index=False)
            else:
                data.to_excel(output_filename, index=False)

        # Show success message when all files are processed
        messagebox.showinfo("Success", f"Files processed successfully")


# Create the application
root = tk.Tk()
app = Application(master=root)
# Start the application main loop
app.mainloop()
