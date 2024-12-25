import tkinter as tk
import os

class input:

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Create and return a new instance of the class if one does not already exist."""
        if cls._instance is None:
            cls._instance = super(input, cls).__new__(cls)
        return cls._instance

    def __init__(self, title, question, answer_type="str", answer_default=None, pattern=None, allow_empty=True, allow_cancel=True, icon=None):
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
        """
        if hasattr(self, 'initialized') and self.initialized:
            self.reinitialize(title, question, answer_type, answer_default, pattern, allow_empty, allow_cancel, icon)
            return
        self.initialized = True
        self.create_window(title, question, answer_type, answer_default, pattern, allow_empty, allow_cancel, icon)

    def reinitialize(self, title, question, answer_type, answer_default, pattern, allow_empty, allow_cancel, icon):
        """Reinitialize the window"""
        if self.root:
            try:
                self.destroy_window()
            except tk.TclError:
                pass
        self.create_window(title, question, answer_type, answer_default, pattern, allow_empty, allow_cancel, icon)

    def create_window(self, title, question, answer_type="str", answer_default=None, pattern=None, allow_empty=True, allow_cancel=True, icon=None):
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
        # Initialize variables
        self.question = question
        self.answer_type = answer_type
        self.allow_empty = allow_empty
        self.answer_default = answer_default
        self.allow_cancel = allow_cancel
        self.pattern = pattern
        self.closed = False
        # Create window
        self.root = tk.Tk() if not tk._default_root else tk.Toplevel()
        if tk._default_root and isinstance(self.root, tk.Toplevel):
            tk._default_root.attributes('-disabled', True)
            self.root.protocol("WM_DELETE_WINDOW", lambda: [self.destroy_window()])
        self.root.withdraw()
        self.root.title(title)
        self.root.resizable(False, False)
        self.root.geometry("+400+250")
        self.root.wm_minsize(250, 50)
        # self.root.wm_attributes('-toolwindow', 'True') # Remove the icon, minimize and maximize buttons
        self.root.attributes('-topmost', True) # Always on top
        self.root.bind("<Key>", self.key_pressed)
        # Validate if the window can be closed
        if self.allow_cancel:
            self.root.protocol("WM_DELETE_WINDOW", self.close)
        else:
            self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        # Frame for the question
        frmLabel = tk.Frame(self.root, background="white")
        if icon:
            imagepath = os.path.join(os.path.dirname(__file__), "images", icon)
            self.root.iconbitmap(imagepath + '.ico')
            self.image = tk.PhotoImage(file=imagepath + '.png')
            titleImg = tk.Label(frmLabel, image=self.image, background="white")
            titleImg.pack(side=tk.LEFT, anchor=tk.N,  padx=(15,3), pady=15)

        wraplength = 400
        titleMsg = tk.Label(frmLabel, text=self.question, background="white", justify=tk.LEFT, wraplength=wraplength)
        titleMsg.pack(side=tk.LEFT, padx=(3,15), pady=15)
        frmLabel.pack(expand=True, fill=tk.BOTH)

        # Frame for the entry
        frmEntry = tk.Frame(self.root, background="white")
        self.answer_entry = tk.Entry(frmEntry, validate="key")
        if self.answer_type == "int":
            self.answer_entry.config(validatecommand=(self.root.register(self.validate_int), '%P'))
        elif self.answer_type == "alphanumeric":
            self.answer_entry.config(validatecommand=(self.root.register(self.validate_alphanumeric), '%P'))
        elif self.answer_type == "float":
            self.answer_entry.config(validatecommand=(self.root.register(self.validate_float), '%P'))
        elif self.answer_type == "password":
            self.answer_entry.config(validatecommand=(self.root.register(self.validate_str), '%P'), show="*")
        else:
            self.answer_entry.config(validatecommand=(self.root.register(self.validate_str), '%P'))
        self.answer_entry.bind("<Key>", self.key_pressed)
        self.answer_entry.focus()
        self.answer_entry.pack(padx=10, pady=(5,15), ipady=3)
        frmEntry.pack(expand=True, fill=tk.BOTH)
        # Frame for the buttons
        frmButtons = tk.Frame(self.root)
        self.button = tk.Button(frmButtons, text="OK", command=self.set_answer)
        if not self.allow_empty:
            self.button.config(state="disabled")
        if self.answer_default is not None:
            self.answer_entry.insert(0, self.answer_default)
            self.answer_entry.select_range(0, tk.END)
        self.button.pack(side=tk.LEFT, padx=10, pady=10, ipadx=3)
        if self.allow_cancel:
            self.buttonCancel = tk.Button(frmButtons, text="Cancel", command=self.close)
            self.buttonCancel.pack(side=tk.LEFT, padx=10, pady=10, ipadx=3)
            self.buttonCancel.bind("<Key>", self.key_pressed)
        if self.pattern is not None:
            self.button.config(state="disabled")
            if self.answer_default is not None:
                self.button.config(state="normal")
            self.answer_entry.bind('<KeyRelease>', self.format_input)
        frmButtons.pack(expand=True)
        # Set focus on the window
        self.root.after(10, lambda: [self.root.focus_force(), self.answer_entry.focus_set()]) # Set focus on the window
        self.root.after(300, lambda: [self.root.focus_force(), self.answer_entry.focus_set()]) # we will make sure it works on slower computers or codes
        # Start the window
        self.root.deiconify() # Show the window
        self.root.mainloop()

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
                self.close()
        # Enter
        elif event.keycode == 13:
            if self.validate_answer():
                self.root.quit()
        # Tab, cycle through buttons
        elif event.keycode == 9:
            widgets = [self.answer_entry, self.button]
            if self.allow_cancel:
                widgets.append(self.buttonCancel)

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

    def close(self):
        """
        Close the window and set the answer to None
        """
        self.closed = True
        if tk._default_root:
            tk._default_root.focus_force()
            tk._default_root.attributes('-disabled', False)
        self.root.destroy()

    def destroy_window(self):
        if self.root:
            self.root.unbind_all("<Key>")
            self.root.unbind_all("<Button-1>")
            self.root.update_idletasks()
            self.root.update()  # Process all pending events
            self.root.destroy()
            self.root.quit()
            if tk._default_root:
                tk._default_root.focus_force()
                tk._default_root.attributes('-disabled', False)

    def set_answer(self):
        """
        Set the answer and close the window
        """
        if self.validate_answer():
            self.root.quit()

    def get_answer(self):
        """
        Get the answer and close the window

        Returns:
            str: answer
        """
        if self.closed:
            return None
        try:
            answer = self.answer_entry.get()
        except tk.TclError:
            return None
        self.root.destroy()
        return answer
