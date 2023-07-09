import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.filenames = None
        self.process_button = None
        self.columns_entry = None
        self.columns_label = None
        self.browse_button = None
        self.filename_label = None
        self.master = master
        self.master.title("Gabe's XSLX Processor")
        self.grid(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        self.filename_label = tk.Label(self, text="No files selected", font=('Helvetica', 9, 'italic'), fg='gray')
        self.filename_label.grid(row=0, column=1, sticky='w')

        self.browse_button = tk.Button(self, text="Browse Excel Files", command=self.load_files, bg='lightblue',
                                       width=20)
        self.browse_button.grid(row=0, column=0, pady=(0, 10))

        self.columns_label = tk.Label(self, text="Columns to remove (comma-separated)", font=('Helvetica', 10))
        self.columns_label.grid(row=1, column=0, sticky='w')

        self.columns_entry = tk.Entry(self, width=40)
        self.columns_entry.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        self.process_button = tk.Button(self, text="Process Files", command=self.process_files, bg='lightgreen',
                                        width=20)
        self.process_button.grid(row=3, column=0, columnspan=2)

    def load_files(self):
        self.filenames = filedialog.askopenfilenames(filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
        if self.filenames:
            self.filename_label['text'] = ', '.join(self.filenames)

    def process_files(self):
        if not self.filenames:
            messagebox.showerror("Error", "No files selected")
            return

        columns_to_remove = self.columns_entry.get().split(',')
        if not columns_to_remove:
            messagebox.showerror("Error", "No columns specified")
            return

        for filename in self.filenames:
            data = pd.read_excel(filename)
            data = data.drop(columns=columns_to_remove, errors='ignore')

            # Save the data to a new file with "_cleaned" appended to the original filename
            base_filename, ext = os.path.splitext(filename)
            output_filename = f"{base_filename}_cleaned{ext}"
            data.to_excel(output_filename, index=False)

        messagebox.showinfo("Success", f"Files processed successfully")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
