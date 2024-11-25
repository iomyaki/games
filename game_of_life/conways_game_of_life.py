import copy
import sys
import tkinter as tk
import tkinter.ttk as ttk


class Cell:
    FILLED_COLOR_BG = "green"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "grey"
    EMPTY_COLOR_BORDER = "grey"

    def __init__(self, master, x, y, size):
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = False
        self.id = None

    def switch(self):
        self.fill = not self.fill

    def draw(self):
        if self.master is not None:
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.id = self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=fill, outline=outline)


class CellGrid(tk.Canvas):
    def __init__(self, master, row_number: int, col_number: int, cell_size: int):
        tk.Canvas.__init__(self, master, width=cell_size * col_number, height=cell_size * row_number)

        self.row_number = row_number
        self.col_number = col_number
        self.cell_size = cell_size

        self.around = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        self.grid = [[Cell(self, j, i, cell_size) for j in range(col_number)] for i in range(row_number)]

        self.cells_alive_old = set()
        self.cells_alive_new = set()
        self.cells_interest = set()

        # memorize the cells that are being modified to avoid many switching of state during the mouse motion
        self.switched_color = set()

        # bind click action
        self.bind("<Button-1>", self.handle_mouse)
        # bind moving while clicking
        self.bind("<B1-Motion>", self.handle_mouse)
        # bind release button action — clear the memory of modified cells
        self.bind("<ButtonRelease-1>", lambda event: self.switched_color.clear())

        # draw
        for row in self.grid:
            for cell in row:
                cell.draw()

    def event_coords(self, event):
        row = int(event.y / self.cell_size)
        col = int(event.x / self.cell_size)
        return row, col

    def handle_mouse(self, event):
        row, col = self.event_coords(event)
        cell = self.grid[row][col]

        if cell not in self.switched_color:
            cell.switch()
            if cell.fill:
                self.cells_alive_old.add((cell.ord, cell.abs))
            else:
                self.cells_alive_old.remove((cell.ord, cell.abs))

            cell.draw()
            self.switched_color.add(cell)

    def update_cells_interest(self):
        for i, j in self.cells_alive_old:
            for di, dj in self.around:
                if 0 <= i + di < self.row_number and 0 <= j + dj < self.col_number:
                    self.cells_interest.add((i + di, j + dj))
            self.cells_interest.add((i, j))

    def iteration(self):
        # delete green rectangles and switch off current living cells
        for i, j in self.cells_alive_old:
            self.delete(self.grid[i][j].id)
            self.grid[i][j].switch()

        # iterate through the interesting cells, calculate new living ones
        for i, j in self.cells_interest:
            alive_around = 0
            for di, dj in self.around:
                if (i + di, j + dj) in self.cells_alive_old:
                    alive_around += 1

            if (i, j) not in self.cells_alive_old and alive_around == 3 or \
                    (i, j) in self.cells_alive_old and 2 <= alive_around <= 3:
                self.cells_alive_new.add((i, j))

        # update the living set
        self.cells_alive_old = copy.deepcopy(self.cells_alive_new)
        self.cells_alive_new.clear()

        # update the interesting set
        self.cells_interest.clear()
        self.update_cells_interest()

        # update the field
        for i, j in self.cells_alive_old:
            self.grid[i][j].switch()

        # redraw the field
        for i, j in self.cells_alive_old:
            self.grid[i][j].draw()


class Game:
    def __init__(self, cell_size: int, delay: int):
        # hyperparameters
        self.cell_size = cell_size
        self.delay = delay

        # grid and other
        self.rows = 0
        self.cols = 0
        self.cancel = None

        # entry
        self.entry = tk.Tk()
        self.rows_var = tk.IntVar()
        self.cols_var = tk.IntVar()

        self.launch_entry()

        # game of life
        self.game_of_life = tk.Tk()
        self.grid = CellGrid(self.game_of_life, self.rows, self.cols, self.cell_size)
        self.start_button = ttk.Button(self.game_of_life, text="Start", command=self.start)
        self.pause_button = ttk.Button(self.game_of_life, text="Pause", command=self.pause, state="disabled")
        self.exit_button = ttk.Button(self.game_of_life, text="Exit", command=sys.exit)

        self.launch_game_of_life()

    def launch_entry(self):
        self.entry.geometry("300x100")

        rows_label = tk.Label(self.entry, text="Number of rows", font=("calibre", 10, "bold"))
        rows_entry = tk.Entry(self.entry, textvariable=self.rows_var, font=("calibre", 10, "normal"))

        cols_label = tk.Label(self.entry, text="Number of columns", font=("calibre", 10, "bold"))
        cols_entry = tk.Entry(self.entry, textvariable=self.cols_var, font=("calibre", 10, "normal"))

        exit_button = tk.Button(self.entry, text="Exit", command=sys.exit)
        submit_button = tk.Button(self.entry, text="Submit", command=self.submit_sizes)

        rows_label.grid(row=0, column=0)
        rows_entry.grid(row=0, column=1)
        cols_label.grid(row=1, column=0)
        cols_entry.grid(row=1, column=1)
        submit_button.grid(row=2, column=0)
        exit_button.grid(row=2, column=1)

        self.entry.mainloop()

    def launch_game_of_life(self):
        self.grid.pack()
        self.exit_button.pack(side=tk.RIGHT)
        self.pause_button.pack(side=tk.RIGHT)
        self.start_button.pack(side=tk.RIGHT)

        self.game_of_life.mainloop()

    def submit_sizes(self):
        self.rows = self.rows_var.get()
        self.cols = self.cols_var.get()
        self.entry.destroy()

    def start(self):
        self.start_button["state"] = "disabled"
        self.pause_button["state"] = "enabled"
        self.grid.update_cells_interest()
        self.game_of_life.after(0, self.proceed)

    def proceed(self):
        self.grid.iteration()
        self.cancel = self.game_of_life.after(self.delay, self.proceed)

    def pause(self):
        self.game_of_life.after_cancel(self.cancel)
        self.start_button["state"] = "enabled"
        self.pause_button["state"] = "disabled"


def main():
    Game(15, 50)


if __name__ == "__main__":
    main()


# make the field toroidal
# delete multiply drawn rectangles
