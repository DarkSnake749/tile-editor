from editor import Editor
from config import *

if __name__ == '__main__':
    app = Editor(WINDOW_SIZE, (8, 8), CELL_SIZE)
    app.run()