import pygame
from config import SELECT_KEY, DRAG_KEY

class Editor:
    def __init__(self, window_size: tuple[int, int], grid_size: tuple[int, int], cell_size: int) -> None:
        # Window setup
        self.__window: pygame.Surface = pygame.display.set_mode(window_size)
        """Surface of the window"""
        pygame.display.set_caption("Tile editor")
        self.__clock: pygame.time.Clock = pygame.time.Clock()

        self.__scale: float = 1.0
    
        self.__grid_size: tuple[int, int] = grid_size
        self.__cell_size = cell_size
        self.__grid: list[pygame.Rect] = self.update_grid((0, 0))

        self.__select_grid: list[bool] = [[False for _ in range(grid_size[0])] for _ in range(grid_size[1])]

        self.__bg_color: str = "black"
        self.__lines_color: str = "green"
        self.__select_line_color: str = "white"

        self.__tools: list[bool] = [True, False]
    
    def update_grid(self, starting_pos: tuple[int, int]) -> pygame.Rect:
        rects: list[pygame.Rect] = []
        for x in range(int(self.__grid_size[0] * self.__scale)):
            for y in range(int(self.__grid_size[1] * self.__scale)):
                rects.append(pygame.Rect(
                    x * self.__cell_size * self.__scale, y * self.__cell_size * self.__scale, 
                    self.__cell_size * self.__scale, self.__cell_size * self.__scale))
        return rects

    def draw(self, grid: list[pygame.Rect], combined_grid: pygame.Rect) -> None:
        for cell in grid:
            pygame.draw.rect(self.__window, self.__lines_color, pygame.Rect(
                cell.x + combined_grid.x, cell.y + combined_grid.y, 
                self.__cell_size * self.__scale, self.__cell_size * self.__scale
            ), 1)
    
    def main_loop(self) -> None:
        drag: bool = False
        drag_offset: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        """Used for the drag of the grid"""
        combined_grid = self.__grid[0].unionall(self.__grid)
        """Where the grid will be drawn"""
        while True:
            # Calculate drag before event
            if not drag:
                drag_offset.x = combined_grid.x - pygame.mouse.get_pos()[0]
                drag_offset.y = combined_grid.y - pygame.mouse.get_pos()[1]

            # Event loop
            for event in pygame.event.get():
                # Quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Key
                if event.type == pygame.KEYDOWN:
                    # Scaling
                    if event.key == pygame.K_EQUALS:
                        self.__scale += .1
                    if event.key == pygame.K_MINUS:
                        self.__scale = self.__scale - .1 if self.__scale > .1 else 0.1
                    
                    # Toggle select tool
                    if event.key == SELECT_KEY:
                        self.__tools = [False for _ in range(len(self.__tools))] 
                        self.__tools[0] = True

                    # Toggle drag tool
                    if event.key == DRAG_KEY:
                        self.__tools = [False for _ in range(len(self.__tools))] 
                        self.__tools[1] = True
                        # Reset drag
                        drag = False if not self.__tools[1] else drag
                
                # Mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    drag = True if self.__tools[1] else False
                    
                
                if event.type == pygame.MOUSEBUTTONUP:
                    drag = False


            # Clear the window
            self.__window.fill(self.__bg_color)

            # Draw
            self.draw(self.__grid, combined_grid)

            if drag:
                combined_grid.x = pygame.mouse.get_pos()[0] + drag_offset.x
                combined_grid.y = pygame.mouse.get_pos()[1] + drag_offset.y 

            # Update
            self.__grid = self.update_grid(combined_grid.topleft)

            # Update the window
            pygame.display.update()
            self.__clock.tick(120)
    
    def run(self) -> None:
        self.main_loop()