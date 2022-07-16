import pickle
import sys
import tkinter as tk
import tkinter.ttk as ttk

from tkrace import AppRace

class AppDay(tk.Frame):
    def __init__(self, races, master=None):
        super().__init__(master)
        self.pack()
        
        self.master.resizable(width=False, height=False)
        self.bgcolor = self.master.cget("background")
        style = ttk.Style()
        style.theme_use("classic")
        style.configure("c.TButton", borderwidth=0, background=self.bgcolor)

        self.races = races

        self.date = races[0][0]

        a = [race[1] for race in races]
        self.racecourses = sorted(set(a), key=a.index)
        # self.plots_filename = "22" + self.dates[0].replace("/", "") + "_plots.png"

        title = "JRA" + " " + self.date + " " + self.racecourses[0]
        self.master.title(title)

        self.status = tk.StringVar()
        self.status.set("")

        self.var_racenames = [tk.StringVar() for _ in range(12)]
        self.var_conditions = [tk.StringVar() for _ in range(12)]
        self.races_at_racecourse = [race for race in races if race[1] == self.racecourses[0]]
        for i, race in enumerate(self.races_at_racecourse):
            self.var_racenames[i].set(" ".join(race[3:4]))
            self.var_conditions[i].set(" ".join(race[4:8]))

        self.frame_upper = tk.Frame(self, width=300, height=300)
        self.frame_lower = tk.Frame(self)
        self.frame_upper.pack(padx=8, anchor=tk.W)
        self.frame_lower.pack(padx=8, pady=4)

        self.create_frame_racecourses()
        self.create_frame_races()

        self.status_bar()

    def create_frame_racecourses(self):
        frame_racecourses = tk.Frame(self.frame_upper, padx=10, pady=10)
        for i, racecourse in enumerate(self.racecourses):
            button = ttk.Button(frame_racecourses, 
                        text=racecourse,
                        style="c.TButton", 
                        command=self.callback_racecourse(i)
            )
            button.pack(side=tk.LEFT, padx=2)  
        button = ttk.Button(
            frame_racecourses,
            text="box plots",
            style="c.TButton",
            command=lambda: self.plots_window(),
        )
        button.pack(side=tk.LEFT, padx=2)
        frame_racecourses.pack(anchor=tk.W)

    def create_frame_races(self):
        length = len(self.var_racenames)
        race_numbers = [str(i).rjust(2, "0") + "R" for i in range(1, length+1)]
        for i, race_num in enumerate(race_numbers):
            frame = tk.Frame(self.frame_lower, padx=12) #, bg="blue")
            button = ttk.Button(
                frame, 
                text=race_num, 
                style="c.TButton",
                command=self.callback_race(i),    
            )
            label_racename = tk.Label(
                frame,
                textvariable=self.var_racenames[i],
                padx=8,
                pady=8,
                width=28,
                anchor=tk.W,
            )
            label_condition = tk.Label(
                frame,
                textvariable=self.var_conditions[i],
                padx=8,
                pady=8, 
                width=26,
                anchor=tk.W, 
            )
            button.pack(side=tk.LEFT)
            label_racename.pack(side=tk.LEFT)
            label_condition.pack()
            frame.pack()

    def callback_racecourse(self, i):
        def func():
            racecourse = self.racecourses[i]
            title = "JRA" + " " + self.date + " " + racecourse
            self.master.title(title)

            self.races_at_racecourse = [race for race in races if race[1] == racecourse]
            for j, race in enumerate(self.races_at_racecourse):
                self.var_racenames[j].set(" ".join(race[3:4]))
                self.var_conditions[j].set(" ".join(race[4:8]))
        return func

    def callback_race(self, i):
        def func():
            race = self.races_at_racecourse[i]
            self.race_window(race)
        return func

    def race_window(self, race):
        root = tk.Toplevel(self)
        app = AppRace(race, master=root)
        app.mainloop()

    def plots_window(self):
        pass
        # root = tk.Toplevel(self)
        # p = "./plots/" + self.plots_filename
        # if os.path.exists(p):
        #     app = AppPlots(p, master=root)
        #     # app.run()

    def status_bar(self):
        statusbar = tk.Label(self, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        statusbar.pack(fill=tk.X)

if __name__ == "__main__":

    p = sys.argv[1]
    with open(p, "rb") as f:
        races = pickle.load(f)

    root = tk.Tk()
    app = AppDay(races, master=root)
    app.mainloop()