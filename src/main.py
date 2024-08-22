from editor import Editor
from config import *

if __name__ == '__main__':
    app = Editor(WINDOW_SIZE, GRID_SIZE, CELL_SIZE)
    app.run()