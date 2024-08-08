import customtkinter as ctk


class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title="Message Box", message=""):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x150")
        self.center_window(400, 150)
        self.grab_set()  # Make the message box modal

        self.label = ctk.CTkLabel(self, text=message, font=("Helvetica", 20), wraplength=280)
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


class CustomMessageBoxWithRetry(CustomMessageBox):
    def __init__(self, parent, title="Message Box", message="", retry_callback=None, quit_callback=None):
        super().__init__(parent, title, message)
        self.geometry("400x200")  # Set the geometry for the retry/quit message box
        self._reconfigure_layout()

        self.retry_callback = retry_callback
        self.quit_callback = quit_callback

    def _reconfigure_layout(self):
        # Clear existing layout
        self.label.pack_forget()
        self.button.pack_forget()

        # Redefine label
        self.label = ctk.CTkLabel(self, text=self.label.cget("text"), font=("Helvetica", 20), wraplength=280)
        self.label.pack(pady=20)

        # Create button frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.retry_button = ctk.CTkButton(self.button_frame, text="Retry", height=30, width=90, command=self.on_retry)
        self.retry_button.pack(side="left", padx=10)

        self.quit_button = ctk.CTkButton(self.button_frame, text="Quit", height=30, width=90, command=self.on_quit)
        self.quit_button.pack(side="right", padx=10)

    def on_retry(self):
        if self.retry_callback:
            self.retry_callback()
        self.destroy()

    def on_quit(self):
        if self.quit_callback:
            self.quit_callback()
        self.destroy()


def show_custom_messagebox_with_retry(parent, title="Message Box", message="", retry_callback=None, quit_callback=None):
    CustomMessageBoxWithRetry(parent, title, message, retry_callback, quit_callback)

