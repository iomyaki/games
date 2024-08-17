import copy
import sys
import tkinter as tk
import tkinter.ttk as ttk


class Cell:
    FILLED_COLOR_BG = "green"
    EMPTY_COLOR_BG = "grey"
    FILLED_COLOR_BORDER = "white"
    EMPTY_COLOR_BORDER = "white"

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = False
        self.id = None

    def switch(self):
        """ Switch if the cell is filled or not. """
        self.fill = not self.fill

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
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
    def __init__(self, master, row_number, col_number, cell_size):
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
        self.bind("<Button-1>", self.handle_mouse_click)
        # bind moving while clicking
        self.bind("<B1-Motion>", self.handle_mouse_motion)
        # bind release button action — clear the memory of modified cells
        self.bind("<ButtonRelease-1>", lambda event: self.switched_color.clear())

        # draw
        for row in self.grid:
            for cell in row:
                cell.draw()

    """
    def create_new_grid(self):
        self.new_grid = [[Cell(self, j, i, self.cell_size) for j in range(self.col_number)] for i in
                         range(self.row_number)]
    """

    def event_coords(self, event):
        row = int(event.y / self.cell_size)
        col = int(event.x / self.cell_size)
        return row, col

    def handle_mouse_click(self, event):
        row, col = self.event_coords(event)
        cell = self.grid[row][col]

        cell.switch()
        if cell.fill:
            self.cells_alive_old.add((cell.ord, cell.abs))
        else:
            self.cells_alive_old.remove((cell.ord, cell.abs))

        cell.draw()
        # add the cell to the list of cell switched during the click
        self.switched_color.add(cell)

    def handle_mouse_motion(self, event):
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

    """
    def initial_scan(self):
        for row in self.grid:
            for cell in row:
                if cell.fill:
                    self.cells_alive_old.add((cell.ord, cell.abs))

        self.upd_interest_set()
    """

    def upd_interest_set(self):
        for i, j in self.cells_alive_old:
            for di, dj in self.around:
                if 0 <= i + di < self.row_number and 0 <= j + dj < self.col_number:
                    self.cells_interest.add((i + di, j + dj))
            self.cells_interest.add((i, j))

    """
    def iteration_old(self):
        self.create_new_grid()

        for i in range(self.row_number):
            for j in range(self.col_number):
                alive_around = 0
                for di, dj in self.around:
                    if (0 <= i + di < self.row_number and
                            0 <= j + dj < self.col_number and
                            self.grid[i + di][j + dj].fill
                    ):
                        alive_around += 1

                if not self.grid[i][j].fill and alive_around == 3 or self.grid[i][j].fill and 2 <= alive_around <= 3:
                    self.new_grid[i][j].switch()

        self.grid = self.new_grid
        self.draw()
    """

    def iteration(self):
        # clear the field
        #self.delete("all")
        for i, j in self.cells_alive_old:
            self.delete(self.grid[i][j].id)  # delete the rectangle geometric figure
            self.grid[i][j].switch()
            #self.grid[i][j].draw()

        # iterate through the interesting cells, calculate new living ones
        for i, j in self.cells_interest:
            alive_around = 0
            for di, dj in self.around:
                if (i + di, j + dj) in self.cells_alive_old:
                    alive_around += 1

            if (i, j) not in self.cells_alive_old and alive_around == 3 or \
                    (i, j) in self.cells_alive_old and 2 <= alive_around <= 3:
                self.cells_alive_new.add((i, j))

        # if new_living is the same as living_cells, there's no need in further iterations

        # update the living set
        self.cells_alive_old = copy.deepcopy(self.cells_alive_new)
        self.cells_alive_new.clear()

        # update the interesting set
        self.cells_interest.clear()
        self.upd_interest_set()

        # update the field
        for i, j in self.cells_alive_old:
            self.grid[i][j].switch()

        # redraw the field
        #self.draw()
        for i, j in self.cells_alive_old:
            self.grid[i][j].draw()

        #print(len(self.living_cells))
        #print(len(self.interest_cells))
        #print(psutil.virtual_memory())
        #print("====================================================")


if __name__ == "__main__":
    def stop():
        sys.exit(0)

    def submit_sizes():
        global rows, cols

        rows = rows_var.get()
        cols = cols_var.get()

        entry.destroy()

    def make_alive():
        grid.iteration()
        g_o_l.after(500, make_alive)  # 50 ms

    def start():
        start_button["state"] = "disabled"
        #grid.initial_scan()
        grid.upd_interest_set()
        g_o_l.after(0, make_alive)

    rows, cols = 0, 0

    # enter the number of rows and columns
    entry = tk.Tk()
    entry.geometry("300x100")

    rows_var = tk.IntVar()
    cols_var = tk.IntVar()

    rows_label = tk.Label(entry, text='Number of rows', font=('calibre', 10, 'bold'))
    rows_entry = tk.Entry(entry, textvariable=rows_var, font=('calibre', 10, 'normal'))

    cols_label = tk.Label(entry, text='Number of columns', font=('calibre', 10, 'bold'))
    cols_entry = tk.Entry(entry, textvariable=cols_var, font=('calibre', 10, 'normal'))

    exit_btn = tk.Button(entry, text='Exit', command=stop)
    sub_btn = tk.Button(entry, text='Submit', command=submit_sizes)

    rows_label.grid(row=0, column=0)
    rows_entry.grid(row=0, column=1)
    cols_label.grid(row=1, column=0)
    cols_entry.grid(row=1, column=1)
    sub_btn.grid(row=2, column=0)
    exit_btn.grid(row=2, column=1)

    entry.mainloop()

    # game of life
    g_o_l = tk.Tk()

    grid = CellGrid(g_o_l, rows, cols, 15)
    start_button = ttk.Button(g_o_l, text='Start', command=start)
    exit_button = ttk.Button(g_o_l, text='Exit', command=stop)

    grid.pack()
    exit_button.pack(side=tk.RIGHT)
    start_button.pack(side=tk.RIGHT)

    g_o_l.mainloop()
