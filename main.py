import tkinter as tk

class PracticeApp:
    def __init__(self, root):# this = reference to the instance of the class, root = reference to the main window
        self.root = root#this.root = root assigns the passed root window to an instance variable, allowing it to be accessed throughout the class
        self.root.title("Grid Practice")
        self.root.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):

        frame = tk.Frame(self.root, bg="lightgreen")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # allow columns and rows to expand
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Entry
        entry = tk.Entry(frame, bg="white")
        entry.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Buttons
        tk.Button(frame, text="Button 1").grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        tk.Button(frame, text="Button 2").grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        tk.Button(frame, text="Button 3").grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        tk.Button(frame, text="Button 4").grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        tk.Button(frame, text="Button 5").grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

root = tk.Tk()# create the main application window using Tkinter's Tk class, which initializes the GUI application
app = PracticeApp(root)# create an instance of the PracticeApp class, passing the root window as an argument
root.mainloop()