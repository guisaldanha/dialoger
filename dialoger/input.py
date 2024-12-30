import tkinter as tk
import os

class input:

    _instance = None

    def __init__(self, title, question, answer_type="str", answer_default=None, pattern=None, allow_empty=True, allow_cancel=True, icon=None, entrance_width=35):
        """Initialize the class

        Args:
            title (str): window title
            question (str): question to be asked
            answer_type (str, optional): type of answer (int, float, alphanumeric, str). Defaults to "str".
            answer_default (_type_, optional): default answer. Defaults to None.
            pattern (str, optional): pattern for the answer. Defaults to None.
            allow_empty (bool, optional): allow empty answer. Defaults to True.
            allow_cancel (bool, optional): allow cancel. Defaults to True.
            icon (str, optional): icon. Defaults to None.
            entrance_width (int, optional): width of the entrance. Defaults to 35.
        """
        if hasattr(self, 'initialized') and self.initialized:
            self.reinitialize(title, question, answer_type, answer_default, pattern, allow_empty, allow_cancel, icon)
            return
        self.initialized = True
        self.answer = None
        self.dialog = None
        self._root = self.find_root()
        self.create_window(title, question, answer_type, answer_default, pattern, allow_empty, allow_cancel, icon, entrance_width)

    def find_root(self):
        """Find or create the root window."""
        if tk._default_root:
            return tk._default_root
        else:
            return None

    def reinitialize(self, title, question, answer_type, answer_default, pattern, allow_empty, allow_cancel, icon):
        """Reinitialize the window"""
        self.destroy_window()
        self.create_window(title, question, answer_type, answer_default, pattern, allow_empty, allow_cancel, icon)

    def create_window(self, title, question, answer_type="str", answer_default=None, pattern=None, allow_empty=True, allow_cancel=True, icon=None, entrance_width=35):
        """
        Create the window

        Args:
            title (str): window title
            question (str): question to be asked
            answer_type (str, optional): type of answer (int, float, alphanumeric, str). Defaults to "str".
            allow_empty (bool, optional): allow empty answer. Defaults to True.
            answer_default (_type_, optional): default answer. Defaults to None.
            allow_cancel (bool, optional): allow cancel. Defaults to True.
        """
        # Create window
        if self._root:
            self.dialog = tk.Toplevel(self._root)
            # Disable the main window
            self._root.attributes('-disabled', True)
        else:
            self.dialog = tk.Tk()

        self.dialog.withdraw()
        # Initialize variables
        self.answer_type = answer_type
        self.allow_empty = allow_empty
        self.allow_cancel = allow_cancel
        self.pattern = pattern

        self.dialog.protocol("WM_DELETE_WINDOW", self.destroy_window)
        self.dialog.title(title)
        self.dialog.resizable(False, False)
        self.dialog.geometry("+400+250")
        self.dialog.attributes('-topmost', True)

        # Message frame
        frm_label = tk.Frame(self.dialog, background="white")
        # Set icon
        if icon:
            imagepath = os.path.join(os.path.dirname(__file__), "images", icon)
            self.dialog.iconbitmap(imagepath + '.ico')
            self.image = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "images", icon + '.png'))
            title_img = tk.Label(frm_label, image=self.image, background="white")
            title_img.image = self.image
            title_img.pack(side=tk.LEFT, anchor=tk.N, padx=(15, 3), pady=15)

        wraplength = 400
        title_msg = tk.Label(frm_label, text=question, background="white", justify=tk.LEFT, wraplength=wraplength)
        title_msg.pack(side=tk.LEFT, padx=(3, 15), pady=15)
        frm_label.pack(expand=True, fill=tk.BOTH)

        # Frame for the entry
        frmEntry = tk.Frame(self.dialog, background="white", padx=30)
        self.answer_entry = tk.Entry(frmEntry, validate="key", width=entrance_width)
        if self.answer_type == "int":
            self.answer_entry.config(validatecommand=(self.dialog.register(self.validate_int), '%P'))
        elif self.answer_type == "alphanumeric":
            self.answer_entry.config(validatecommand=(self.dialog.register(self.validate_alphanumeric), '%P'))
        elif self.answer_type == "float":
            self.answer_entry.config(validatecommand=(self.dialog.register(self.validate_float), '%P'))
        elif self.answer_type == "password":
            self.answer_entry.config(validatecommand=(self.dialog.register(self.validate_str), '%P'), show="*")
        else:
            self.answer_entry.config(validatecommand=(self.dialog.register(self.validate_str), '%P'))
        self.answer_entry.bind("<Key>", self.key_pressed)
        self.answer_entry.focus()
        self.answer_entry.pack(padx=10, pady=(5,15), ipady=3)
        frmEntry.pack(expand=True, fill=tk.BOTH)

        # Frame for the buttons
        frmButtons = tk.Frame(self.dialog)
        self.button = tk.Button(frmButtons, text="OK", command=self.set_answer)
        self.button.bind("<Key>", self.key_pressed)
        if not self.allow_empty:
            self.button.config(state="disabled")
        if answer_default is not None:
            self.answer_entry.insert(0, answer_default)
            self.answer_entry.select_range(0, tk.END) # Deixa o texto selecionado
        self.button.pack(side=tk.LEFT, padx=10, pady=10, ipadx=3)
        if self.pattern is not None:
            self.button.config(state="disabled")
            if answer_default is not None:
                self.button.config(state="normal")
            self.answer_entry.bind('<KeyRelease>', self.format_input)
        if self.allow_cancel:
            self.buttonCancel = tk.Button(frmButtons, text="Cancel", command=self.destroy_window)
            self.buttonCancel.pack(side=tk.LEFT, padx=10, pady=10, ipadx=3)
            self.buttonCancel.bind("<Key>", self.key_pressed)
        frmButtons.pack(expand=True)

        # Update layout and show the window
        self.dialog.update_idletasks()

        # Set focus on the window
        self.dialog.after(10, lambda: [self.dialog.focus_force(), self.answer_entry.focus_set()])
        self.dialog.after(300, lambda: [self.dialog.focus_force(), self.answer_entry.focus_set()])

        # Start the window
        self.dialog.deiconify() # Show the window
        self.dialog.wait_window()

    def format_input(self, event):
        """Format the input according to the pattern"""
        if event.keysym in ["Left", "Right", "Up", "Down", "Shift_L", "Shift_R", "Control_L", "Control_R"]:
            return

        input = ''.join([c for c in self.answer_entry.get() if c.isdigit()])
        partial = ''
        for char in self.pattern:
            if char == '#':
                if input:
                    partial += input[0]
                    input = input[1:]
                else:
                    partial += '#'
            else:
                partial += char

        # Replaces all # with empty
        result = ''.join([c for c in partial if c != '#'])

        # while the last character is not a number, remove the last character
        while len(result) > 0 and not result[-1].isdigit():
            result = result[:-1]

        # updates the entry's content with the formatted entry
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.insert(0, result)

        if len(self.answer_entry.get()) != len(self.pattern):
            self.button.config(state="disabled")
        else:
            self.button.config(state="normal")

    def validate_int(self, value):
        """
        Validate if the value is an integer

        Args:
            value (str): value to be validated

        Returns:
            bool: True if the value is an integer, False otherwise
        """
        if value.isdigit() or value == "":
            self.button.config(state="normal")
            return True
        else:
            return False

    def validate_alphanumeric(self, value):
        """
        Validate if the value is alphanumeric

        Args:
            value (str): value to be validated

        Returns:
            bool: True if the value is alphanumeric, False otherwise
        """
        if value.isalnum() or value == "":
            self.button.config(state="normal")
            return True
        else:
            return False

    def validate_float(self, value):
        """
        Validate if the value is a float

        Args:
            value (str): value to be validated

        Returns:
            bool: True if the value is a float, False otherwise
        """
        if value.replace(".", "").isdigit() or value == "":
            self.button.config(state="normal")
            return True
        else:
            return False

    def validate_str(self, value):
        """
        Validate if the value is a string

        Args:
            value (str): value to be validated

        Returns:
            bool: True if the value is a string, False otherwise
        """
        self.button.config(state="normal")
        return True

    def key_pressed(self, event):
        """
        Handles keystrokes in the window for UI updates

        Args:
            event (event): key press event
        """
        # Escape
        if event.keycode == 27:
            if self.allow_cancel:
                self.destroy_window()
        # Enter
        elif event.keycode == 13:
            if self.validate_answer():
                self.set_answer()
        # Tab, cycle through buttons
        elif event.keycode == 9:
            widgets = [self.answer_entry, self.button]
            current_index = widgets.index(event.widget)
            next_index = (current_index + 1) % len(widgets)
            widgets[next_index].focus_set()
            return "break"  # Prevent default behavior
        else:
            pass

    def validate_answer(self):
        """
        Validate the answer

        Returns:
            bool: True if the answer is valid, False otherwise
        """
        if not self.allow_empty and self.answer_entry.get() == "":
            return False
        if self.answer_type == "int" and not self.answer_entry.get().isdigit():
            return False
        if self.answer_type == "alphanumeric" and not self.answer_entry.get().isalnum():
            return False
        if self.answer_type == "float" and not self.answer_entry.get().replace(".", "").isdigit():
            return False
        if self.pattern is not None:
            if len(self.answer_entry.get()) != len(self.pattern):
                return False
        return True

    def destroy_window(self):
        """Destroy the window and re-enable the root"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        input._instance = None
        if self._root:
            self._root.attributes('-disabled', False)
            self._root.focus_force()

    def set_answer(self):
        """
        Set the answer and close the window
        """
        if self.validate_answer():
            self.answer = self.answer_entry.get()
            self.destroy_window()
