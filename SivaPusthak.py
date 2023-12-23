import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import csv

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SivaPusthak Library Management System")

        # Load images
        self.logo = Image.open("logo.png")  # Replace "logo.png" with your logo file
        self.logo = ImageTk.PhotoImage(self.logo)

        self.cover_placeholder = Image.open("cover_placeholder.jpg")  # Replace "cover_placeholder.jpg" with a default cover image
        self.cover_placeholder = ImageTk.PhotoImage(self.cover_placeholder)

        # Create a treeview to display book details
        self.tree = ttk.Treeview(self.root, columns=("Title", "Author", "Genre"))
        self.tree.heading("#0", text="Cover")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Genre", text="Genre")
        self.tree.column("#0", width=100)

        self.tree.pack(padx=10, pady=10)

        # Add sample data (replace this with your data loading logic)
        self.add_book("Book 1", "Author 1", "Fiction", "cover1.jpg")
        self.add_book("Book 2", "Author 2", "Non-fiction", "cover2.jpg")

        # Add buttons for actions
        add_button = tk.Button(root, text="Add Book", command=self.add_book_window)
        add_button.pack(pady=5)

        remove_button = tk.Button(root, text="Remove Book", command=self.remove_book)
        remove_button.pack(pady=5)

        import_button = tk.Button(root, text="Import Books from CSV", command=self.import_books)
        import_button.pack(pady=5)

        # Display the logo
        logo_label = tk.Label(root, image=self.logo)
        logo_label.pack()

    def add_book_window(self):
        # Create a new window for adding a book
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Book")

        # Create entry fields for book details
        title_label = tk.Label(add_window, text="Title:")
        title_label.grid(row=0, column=0, padx=10, pady=10)
        title_entry = tk.Entry(add_window)
        title_entry.grid(row=0, column=1, padx=10, pady=10)

        author_label = tk.Label(add_window, text="Author:")
        author_label.grid(row=1, column=0, padx=10, pady=10)
        author_entry = tk.Entry(add_window)
        author_entry.grid(row=1, column=1, padx=10, pady=10)

        genre_label = tk.Label(add_window, text="Genre:")
        genre_label.grid(row=2, column=0, padx=10, pady=10)
        genre_entry = tk.Entry(add_window)
        genre_entry.grid(row=2, column=1, padx=10, pady=10)

        cover_label = tk.Label(add_window, text="Cover Image:")
        cover_label.grid(row=3, column=0, padx=10, pady=10)
        cover_entry = tk.Entry(add_window)
        cover_entry.grid(row=3, column=1, padx=10, pady=10)

        # Function to add a book to the treeview
        def add_book():
            title = title_entry.get()
            author = author_entry.get()
            genre = genre_entry.get()
            cover = cover_entry.get() if cover_entry.get() else "cover_placeholder.jpg"
            self.add_book(title, author, genre, cover)
            add_window.destroy()

        # Button to add the book
        add_button = tk.Button(add_window, text="Add", command=add_book)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

    def add_book(self, title, author, genre, cover):
        # Add a book to the treeview
        self.tree.insert("", "end", text=title, values=(title, author, genre), tags=(cover,))
        # You may want to load the cover image here and display it in the treeview

    def remove_book(self):
        # Remove the selected book from the treeview
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item[0])

    def import_books(self):
        # Open a file dialog to select a CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        # Check if a file was selected
        if file_path:
            # Clear existing entries in the treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Read data from the CSV file and add books to the treeview
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    title, author, genre, cover = row
                    self.add_book(title, author, genre, cover)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
