import tkinter as tk
import os

class input:
    def __init__(self, title, question, answer_type="str", answer_default=None, pattern=None, allow_empty=True, allow_cancel=True, icon=None):
        """
        Initialize the window

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
        self.root = tk.Tk()
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
            image = tk.PhotoImage(file=imagepath + '.png')
            titleImg = tk.Label(frmLabel, image=image, background="white")
            titleImg.pack(side=tk.LEFT, anchor=tk.N,  padx=(15,3), pady=15)

        wraplength = 400
        titleMsg = tk.Label(frmLabel, text=self.question, background="white", justify=tk.LEFT, wraplength=wraplength)
        titleMsg.pack(side=tk.LEFT, padx=(3,15), pady=15)
        frmLabel.pack(expand=True, fill=tk.BOTH)

        # Frame for the entry
        frmEntry = tk.Frame(self.root, background="white")
        self.entry = tk.Entry(frmEntry, validate="key")
        if self.answer_type == "int":
            self.entry.config(validatecommand=(self.root.register(self.validate_int), '%P'))
        elif self.answer_type == "alphanumeric":
            self.entry.config(validatecommand=(self.root.register(self.validate_alphanumeric), '%P'))
        elif self.answer_type == "float":
            self.entry.config(validatecommand=(self.root.register(self.validate_float), '%P'))
        elif self.answer_type == "password":
            self.entry.config(validatecommand=(self.root.register(self.validate_str), '%P'), show="*")
        else:
            self.entry.config(validatecommand=(self.root.register(self.validate_str), '%P'))
        self.entry.bind("<Key>", self.key_pressed)
        self.entry.focus()
        self.entry.pack(padx=10, pady=(5,15), ipady=3)
        frmEntry.pack(expand=True, fill=tk.BOTH)
        # Frame for the buttons
        frmButtons = tk.Frame(self.root)
        self.button = tk.Button(frmButtons, text="OK", command=self.set_answer)
        if not self.allow_empty:
            self.button.config(state="disabled")
        if self.answer_default is not None:
            self.entry.insert(0, self.answer_default)
            self.entry.select_range(0, tk.END)
        self.button.pack(side=tk.LEFT, padx=10, pady=10, ipadx=3)
        if self.allow_cancel:
            self.buttonCancel = tk.Button(frmButtons, text="Cancel", command=self.close)
            self.buttonCancel.pack(side=tk.LEFT, padx=10, pady=10, ipadx=3)
            self.buttonCancel.bind("<Key>", lambda event: self.close())
        if self.pattern is not None:
            self.button.config(state="disabled")
            self.entry.bind('<KeyRelease>', self.format_input)
        frmButtons.pack(expand=True)
        # Set focus on the window
        self.root.after(300, lambda: [self.root.focus_force(), self.entry.focus_set()])
        # Start the window
        self.root.mainloop()

    def format_input(self, event):
        """Format the input according to the pattern"""
        input = ''.join([c for c in self.entry.get() if c.isdigit()])
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
        self.entry.delete(0, tk.END)
        self.entry.insert(0, result)

        if len(self.entry.get()) != len(self.pattern):
            self.button.config(state="disabled")

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
        if event.keycode == 13:
            if self.validate_answer():
                self.root.quit()

    def validate_answer(self):
        """
        Validate the answer

        Returns:
            bool: True if the answer is valid, False otherwise
        """
        if not self.allow_empty and self.entry.get() == "":
            return False
        if self.answer_type == "int" and not self.entry.get().isdigit():
            return False
        if self.answer_type == "alphanumeric" and not self.entry.get().isalnum():
            return False
        if self.answer_type == "float" and not self.entry.get().replace(".", "").isdigit():
            return False
        if self.pattern is not None:
            if len(self.entry.get()) != len(self.pattern):
                return False
        return True

    def close(self):
        """
        Close the window and set the answer to None
        """
        self.closed = True
        self.root.destroy()

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
        answer = self.entry.get()
        self.root.destroy()
        return answer
