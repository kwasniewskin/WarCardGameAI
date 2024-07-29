import customtkinter as ctk


class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title="Message Box", message=""):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.center_window(400, 200)
        self.grab_set()  # Make the message box modal

        self.label = ctk.CTkLabel(self, text=message,font=("Helvetica", 32), wraplength=280)
        self.label.pack(pady=20)

        self.button = ctk.CTkButton(self, text="OK", height=30, width=200, command=self.on_ok)
        self.button.pack(pady=10)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def on_ok(self):
        self.destroy()


def show_custom_messagebox(parent, title="Message Box", message=""):
    CustomMessageBox(parent, title, message)
