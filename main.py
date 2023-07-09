import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os


# Define the main application class that inherits from tkinter's Frame class
class Application(tk.Frame):
    # Initialize the Application class
    def __init__(self, master=None):
        super().__init__(master)

        # Variable to hold selected files names
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
        self.master.title("Gabe's XSLX Processor")

        # Arrange this Frame widget in a grid layout with padding
        self.grid(padx=10, pady=10)

        # Create UI elements
        self.create_widgets()

    # Method to create and configure widgets
    def create_widgets(self):
        # Label for showing selected file names
        self.filename_label = tk.Label(self, text="No files selected", font=('Helvetica', 9, 'italic'), fg='gray')
        self.filename_label.grid(row=0, column=1, sticky='w')

        # Button for browsing and selecting Excel files
        self.browse_button = tk.Button(self, text="Browse Excel Files", command=self.load_files, bg='lightblue',
                                       width=20)
        self.browse_button.grid(row=0, column=0, pady=(0, 10))

        # Label for input field (Entry widget) for column names to remove
        self.columns_label = tk.Label(self, text="Columns to remove (comma-separated)", font=('Helvetica', 10))
        self.columns_label.grid(row=1, column=0, sticky='w')

        # Entry widget for column names input
        self.columns_entry = tk.Entry(self, width=40)
        self.columns_entry.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        # Button for processing files
        self.process_button = tk.Button(self, text="Process Files", command=self.process_files, bg='lightgreen',
                                        width=20)
        self.process_button.grid(row=3, column=0, columnspan=2)

    # Method to load files, triggered by "Browse Excel Files" button
    def load_files(self):
        # Open a file dialog and get the selected filenames
        self.filenames = filedialog.askopenfilenames(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        if self.filenames:
            # Update the filename label text with selected files
            self.filename_label['text'] = ', '.join(self.filenames)

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
            # Load the data from Excel file
            data = pd.read_excel(filename)
            # Remove the specified columns
            data = data.drop(columns=columns_to_remove, errors='ignore')

            # Save the data to a new file with "_cleaned" appended to the original filename
            base_filename, ext = os.path.splitext(filename)
            output_filename = f"{base_filename}_cleaned{ext}"
            data.to_excel(output_filename, index=False)

        # Show success message when all files are processed
        messagebox.showinfo("Success", f"Files processed successfully")


# Create the application
root = tk.Tk()
app = Application(master=root)
# Start the application main loop
app.mainloop()
