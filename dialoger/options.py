import tkinter as tk
import os

class options():

    def __init__(self, title:str, message:str, choices:list, icon=None) -> None:
        """
        Initialize the window

        Args:
            title (str): window title
            message (str): message to be shown
            choices (list): list of choices
        """
        # Create window
        self.root = tk.Tk()
        self.root.title(title)
        self.root.resizable(False, False)
        self.root.geometry("+400+250")
        self.root.wm_minsize(250, 50)
        self.root.attributes('-topmost', True) # Always on top
        # self.root.wm_attributes('-toolwindow', 'True') # Remove the icon, minimize and maximize buttons
        self.root.protocol("WM_DELETE_WINDOW", self.close())
        self.root.bind("<Key>", self.key_pressed_in_root)
        # Frame for the message
        frmLabel = tk.Frame(self.root, background="white")
        if icon:
            imagepath = os.path.join(os.path.dirname(__file__), "images", icon)
            self.root.iconbitmap(imagepath + '.ico')
            image = tk.PhotoImage(file=imagepath + '.png')
            titleImg = tk.Label(frmLabel, image=image, background="white")
            titleImg.pack(side=tk.LEFT, anchor=tk.N,  padx=(15,3), pady=15)

        wraplength = 400 if len(choices) < 3 else 650

        titleMsg = tk.Label(frmLabel, text=message, background="white", justify=tk.LEFT, wraplength=wraplength)
        titleMsg.pack(side=tk.LEFT, padx=(3,15), pady=15)

        frmLabel.pack(expand=True, fill=tk.BOTH)
        # Frame for the buttons
        frmButtons = tk.Frame(self.root)
        self.buttons = []
        for choice in choices:
            self.buttons.append(tk.Button(frmButtons, text=choice, borderwidth = 1, command=lambda x=choice: self.set_choice(self.root, x)))
            self.buttons[-1].bind("<Key>", self.button_pressed_key)
            self.buttons[-1].pack(side=tk.LEFT, padx=10, pady=10, ipadx=5, ipady=1)
        self.buttons[0].focus_set()
        frmButtons.pack(expand=True)
        # Set focus on the window
        self.root.after(300, lambda: [self.root.focus_force(), self.buttons[0].focus_set()])
        # Start the window
        self.root.mainloop()


    def set_choice(self, root:tk.Tk, choice:str) -> str:
        """
        Set the choice and close the window

        Args:
            root (tkinter.Tk): root window
            choice (str): choice

        Returns:
            str: choice
        """
        self.choice = choice
        root.destroy()
        return choice

    def close(self):
        """
        Close the window and set the choice to None
        """
        self.choice = None

    def key_pressed_in_root(self, event):
        """
        Handles keystrokes in the window for UI updates

        Args:
            event (event): key press event
        """
        # Escape
        if event.keycode == 27:
            self.root.destroy()

    def button_pressed_key(self, event):
        """
        Handles button key presses for UI updates

        Args:
            event (event): key press event
        """
        # Enter
        if event.keycode == 13:
            self.set_choice(self.root, event.widget['text'])
        # Down or Right
        if event.keycode == 40 or event.keycode == 39:
            self.next_button(event.widget)
        # Up or Left
        if event.keycode == 38 or event.keycode == 37:
            self.previous_button(event.widget)

    def next_button(self, button):
        """
        Select the next button

        Args:
            button (button): current button
        """
        i = self.buttons.index(button)
        if i < len(self.buttons) - 1:
            self.buttons[i + 1].focus_set()
        else:
            self.buttons[0].focus_set()

    def previous_button(self, button):
        """
        Sekect the previous button

        Args:
            button (button): current button
        """
        i = self.buttons.index(button)
        if i > 0:
            self.buttons[i - 1].focus_set()
        else:
            self.buttons[-1].focus_set()
