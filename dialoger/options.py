import tkinter as tk
import os

class options():

    _instance = None

    def __init__(self, title: str, message: str, choices: list, icon=None, orientation='horizontal') -> None:
        """Initialize the class

        Args:
            title (str): window title
            message (str): message to be shown
            choices (list): list of choices
            icon (str): icon file name
        """
        if hasattr(self, 'initialized') and self.initialized:
            self.reinitialize(title, message, choices, icon)
            return
        self.orientation = orientation
        self.initialized = True
        self.choice = None
        self.dialog = None
        self._root = self.find_root()
        self.create_window(title, message, choices, icon)

    def find_root(self):
        """Find or create the root window."""
        if tk._default_root:
            return tk._default_root
        else:
            return None

    def reinitialize(self, title, message, choices, icon):
        """Reinitialize the window"""
        self.destroy_window()
        self.create_window(title, message, choices, icon)

    def create_window(self, title, message, choices, icon):
        """
        Create the window

        Args:
            title (str): window title
            message (str): message to be shown
            choices (list): list of choices
            icon (str): icon file name
        """
        # Create window
        if self._root:
            self.dialog = tk.Toplevel(self._root)
            self._root.attributes('-disabled', True)
        else:
            self.dialog = tk.Tk()

        self.dialog.withdraw()

        self.dialog.protocol("WM_DELETE_WINDOW", self.close)
        self.dialog.title(title)
        self.dialog.resizable(False, False)
        self.dialog.geometry("+400+250")
        self.dialog.attributes('-topmost', True)

        # Set icon
        if icon:
            imagepath = os.path.join(os.path.dirname(__file__), "images", icon)
            self.dialog.iconbitmap(imagepath + '.ico')

        # Message frame
        frm_label = tk.Frame(self.dialog, background="white")
        if icon:
            self.image = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "images", icon + '.png'))
            title_img = tk.Label(frm_label, image=self.image, background="white")
            title_img.image = self.image
            title_img.pack(side=tk.LEFT, anchor=tk.N, padx=(15, 3), pady=15)

        wraplength = 400 if len(choices) < 3 else 650
        title_msg = tk.Label(frm_label, text=message, background="white", justify=tk.LEFT, wraplength=wraplength)
        title_msg.pack(side=tk.LEFT, padx=(3, 15), pady=15)
        frm_label.pack(expand=True, fill=tk.BOTH)

        # Button frame
        frmButtons = tk.Frame(self.dialog)
        self.buttons = []
        for choice in choices:
            btn = tk.Button(frmButtons, text=choice, borderwidth=1, command=lambda x=choice: self.set_choice(x))

            btn.bind("<Right>", lambda event, button=btn: self.next_button(button))
            btn.bind("<Left>", lambda event, button=btn: self.previous_button(button))
            btn.bind("<Return>", lambda event, button=btn: self.set_choice(button['text']))
            btn.bind("<Escape>", lambda event: self.close())
            side_option = tk.TOP if self.orientation == 'vertical' else tk.LEFT
            btn.pack(side=side_option, padx=10, pady=10, ipadx=5, ipady=1)
            self.buttons.append(btn)
        self.buttons[0].focus_set()
        frmButtons.pack(expand=True)

        # Update layout and show the window
        self.dialog.update_idletasks()

        # Focus settings
        self.dialog.after(10, lambda: [self.dialog.focus_force(), self.buttons[0].focus_set()])
        self.dialog.after(300, lambda: [self.dialog.focus_force(), self.buttons[0].focus_set()])
        self.dialog.deiconify()
        self.dialog.bind("<Key>", self.key_pressed_in_root)
        self.dialog.wait_window()


    def set_choice(self, choice: str) -> None:
        """Set the choice and close the window"""
        self.choice = choice
        self.destroy_window()

    def close(self):
        """Close the window and set the choice to None"""
        self.choice = None
        self.destroy_window()

    def destroy_window(self):
        """Destroy the window and re-enable the root"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        options._instance = None
        if self._root:
            self._root.attributes('-disabled', False)
            self._root.focus_force()

    def key_pressed_in_root(self, event):
        """Handle Escape key press to close the dialog"""
        if event.keysym == 'Escape':
            self.close()

    def next_button(self, button):
        """Select the next button"""
        i = self.buttons.index(button)
        self.buttons[(i + 1) % len(self.buttons)].focus_set()

    def previous_button(self, button):
        """Select the previous button"""
        i = self.buttons.index(button)
        self.buttons[(i - 1) % len(self.buttons)].focus_set()
