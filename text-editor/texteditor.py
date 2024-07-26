import tkinter as tk
from tkinter import filedialog, colorchooser, simpledialog, messagebox
from cryptography.fernet import Fernet
from datetime import datetime
import os
import json

class TextEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Python Text Editor")

        self.default_font_size = 12
        self.cursor_color = "#000000"  # Default cursor color
        self.current_file = None
        self.password = None
        self.key = None

        self.text_area = tk.Text(self.window, wrap=tk.WORD, font=("Arial", self.default_font_size), insertbackground=self.cursor_color)
        self.text_area.pack(expand=tk.YES, fill=tk.BOTH)

        self.create_menu()
        self.create_status_bar()
        self.bind_shortcuts()

        self.update_cursor_position()  # Initial update

        self.load_theme_settings()  # Load theme settings after text_area is initialized

        self.window.mainloop()


    def create_menu(self):
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)

        # File menu
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="New Window", command=self.new_window, accelerator="Ctrl+Shift+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_command(label="Save All", command=self.save_all_files, accelerator="Ctrl+Alt+S")
        file_menu.add_command(label="Set Password", command=self.set_password)
        file_menu.add_command(label="Remove Password", command=self.remove_password)
        file_menu.add_separator()
        file_menu.add_command(label="Close Window", command=self.window.quit, accelerator="Ctrl+Shift+W")
        file_menu.add_command(label="Exit", command=self.window.quit)

        # Edit menu
        edit_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_command(label="Delete", command=self.delete, accelerator="Del")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.find, accelerator="Ctrl+F")
        edit_menu.add_command(label="Find Next", command=self.find_next, accelerator="F3")
        edit_menu.add_command(label="Find Previous", command=self.find_previous, accelerator="Shift+F3")
        edit_menu.add_command(label="Replace", command=self.replace, accelerator="Ctrl+H")
        edit_menu.add_command(label="Go To", command=self.go_to, accelerator="Ctrl+G")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Time/Date", command=self.time_date, accelerator="F5")

        # View menu
        view_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Word Wrap", command=self.toggle_word_wrap)
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+-")

        # Theme menu
        theme_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Change Theme Color", command=self.change_theme_color)
        theme_menu.add_command(label="Change Text Color", command=self.change_text_color)
        theme_menu.add_command(label="Change Cursor Color", command=self.change_cursor_color)
        theme_menu.add_command(label="Change Opacity", command=self.change_opacity)

    def create_status_bar(self):
        self.status_bar = tk.Label(self.window, text="Line: 1, Column: 1", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.bind("<Motion>", self.update_cursor_position)  # Bind cursor movement

    def bind_shortcuts(self):
        self.window.bind("<Control-n>", lambda event: self.new_file())
        self.window.bind("<Control-Shift-N>", lambda event: self.new_window())
        self.window.bind("<Control-o>", lambda event: self.open_file())
        self.window.bind("<Control-s>", lambda event: self.save_file())
        self.window.bind("<Control-Shift-s>", lambda event: self.save_as_file())
        self.window.bind("<Control-Alt-s>", lambda event: self.save_all_files())
        self.window.bind("<Control-w>", lambda event: self.window.quit())
        self.window.bind("<Control-Shift-w>", lambda event: self.window.quit())
        self.window.bind("<Control-z>", lambda event: self.undo())
        self.window.bind("<Control-y>", lambda event: self.redo())
        self.window.bind("<Control-x>", lambda event: self.cut())
        self.window.bind("<Control-c>", lambda event: self.copy())
        self.window.bind("<Control-v>", lambda event: self.paste())
        self.window.bind("<Delete>", lambda event: self.delete())
        self.window.bind("<Control-f>", lambda event: self.find())
        self.window.bind("<F3>", lambda event: self.find_next())
        self.window.bind("<Shift-F3>", lambda event: self.find_previous())
        self.window.bind("<Control-h>", lambda event: self.replace())
        self.window.bind("<Control-g>", lambda event: self.go_to())
        self.window.bind("<Control-a>", lambda event: self.select_all())
        self.window.bind("<F5>", lambda event: self.time_date())
        self.window.bind("<Control-plus>", lambda event: self.zoom_in())
        self.window.bind("<Control-minus>", lambda event: self.zoom_out())

    def update_cursor_position(self, event=None):
        # Get cursor position
        index = self.text_area.index(tk.INSERT)
        line, column = map(int, index.split('.'))
        # Update status bar with cursor position
        self.status_bar.config(text=f"Line: {line}, Column: {column}")

    # File menu commands
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.password = None
        self.key = None

    def new_window(self):
        new_window = tk.Toplevel(self.window)
        TextEditor()

    def open_file(self):
        file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            self.current_file = file
            self.key = self.load_key()

            if self.is_password_protected(file):
                self.prompt_for_password(file)
            else:
                self.load_file(file)

    def save_file(self):
        if self.current_file:
            content = self.text_area.get(1.0, tk.END)
            if self.password:
                # Encrypt the file content
                encrypted_content = self.encrypt(content)
                with open(self.current_file, "wb") as file_handler:
                    file_handler.write(encrypted_content)
            else:
                # Save the file as is
                with open(self.current_file, "w") as file_handler:
                    file_handler.write(content)
            self.window.title(f"Python Text Editor - {self.current_file}")

    def save_as_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            self.current_file = file
            self.save_file()

    def save_all_files(self):
        # Implement saving all open files if tabs/multiple files are added
        pass

    def set_password(self):
        if self.current_file:
            password = simpledialog.askstring("Set Password", "Enter password:")
            if password:
                self.password = password
                self.key = Fernet.generate_key()
                self.save_key()
                messagebox.showinfo("Success", "Password set successfully.")
                self.save_file()

    def remove_password(self):
        if self.current_file:
            self.password = None
            self.key = None
            self.save_key()
            messagebox.showinfo("Success", "Password protection removed.")
            self.save_file()

    def is_password_protected(self, file):
        # Check if a key exists for the file
        key_file = file + ".key"
        return os.path.exists(key_file)

    def save_key(self):
        if self.key:
            key_file = self.current_file + ".key"
            with open(key_file, "wb") as keyfile:
                keyfile.write(self.key)

    def load_key(self):
        key_file = self.current_file + ".key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as keyfile:
                self.key = keyfile.read()
            return Fernet(self.key)
        return None

    def prompt_for_password(self, file):
        entered_password = simpledialog.askstring("Password", "Enter password:")
        if entered_password == self.password:
            self.load_file(file)
        else:
            messagebox.showerror("Error", "Incorrect password.")
            self.current_file = None

    def encrypt(self, data):
        fernet = Fernet(self.key)
        return fernet.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        fernet = Fernet(self.key)
        return fernet.decrypt(encrypted_data).decode()

    def load_file(self, file):
        with open(file, "rb") as file_handler:
            encrypted_content = file_handler.read()
            content = self.decrypt(encrypted_content) if self.key else encrypted_content.decode()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.INSERT, content)
        self.window.title(f"Python Text Editor - {file}")

    # Edit menu commands
    def undo(self):
        self.text_area.event_generate("<<Undo>>")

    def redo(self):
        self.text_area.event_generate("<<Redo>>")

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def delete(self):
        self.text_area.delete("sel.first", "sel.last")

    def find(self):
        # Implement find functionality here
        pass

    def find_next(self):
        # Implement find next functionality here
        pass

    def find_previous(self):
        # Implement find previous functionality here
        pass

    def replace(self):
        # Implement replace functionality here
        pass

    def go_to(self):
        # Implement go to functionality here
        pass

    def select_all(self):
        self.text_area.tag_add("sel", "1.0", "end")

    def time_date(self):
        self.text_area.insert(tk.INSERT, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # View menu commands
    def toggle_word_wrap(self):
        if self.text_area.cget("wrap") == tk.WORD:
            self.text_area.config(wrap=tk.NONE)
        else:
            self.text_area.config(wrap=tk.WORD)

    def zoom_in(self):
        self.default_font_size += 2
        self.text_area.config(font=("Arial", self.default_font_size))

    def zoom_out(self):
        self.default_font_size = max(2, self.default_font_size - 2)
        self.text_area.config(font=("Arial", self.default_font_size))

    # Theme menu commands
    def change_theme_color(self):
        color = colorchooser.askcolor(title="Choose Theme Color")[1]
        if color:
            self.text_area.config(bg=color)
            self.save_theme_settings()

    def change_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            self.text_area.config(fg=color)
            self.save_theme_settings()

    def change_cursor_color(self):
        color = colorchooser.askcolor(title="Choose Cursor Color")[1]
        if color:
            self.cursor_color = color
            self.text_area.config(insertbackground=self.cursor_color)
            self.save_theme_settings()

    def change_opacity(self):
        opacity = simpledialog.askfloat("Opacity", "Enter opacity value (0.0 - 1.0):", minvalue=0.0, maxvalue=1.0)
        if opacity is not None:
            self.window.attributes("-alpha", opacity)
            self.save_theme_settings()

    def save_theme_settings(self):
        settings = {
            "bg_color": self.text_area.cget("bg"),
            "fg_color": self.text_area.cget("fg"),
            "cursor_color": self.cursor_color,
            "opacity": self.window.attributes("-alpha")
        }
        with open("theme_settings.json", "w") as f:
            json.dump(settings, f)

    def load_theme_settings(self):
        if os.path.exists("theme_settings.json"):
            with open("theme_settings.json", "r") as f:
                settings = json.load(f)
                self.text_area.config(bg=settings.get("bg_color", "#FFFFFF"), fg=settings.get("fg_color", "#000000"))
                self.cursor_color = settings.get("cursor_color", "#000000")
                self.text_area.config(insertbackground=self.cursor_color)
                self.window.attributes("-alpha", settings.get("opacity", 1.0))

if __name__ == "__main__":
    text_editor = TextEditor()
