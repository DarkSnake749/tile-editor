import pygame

class Editor:
    def __init__(self, window_size: tuple[int, int], grid_size: tuple[int, int], cell_size: int) -> None:
        # Window setup
        self.__window: pygame.Surface = pygame.display.set_mode(window_size)
        """Surface of the window"""
        pygame.display.set_caption("Tile editor")
        self.__clock: pygame.time.Clock = pygame.time.Clock()
    
        self.__grid_size: tuple[int, int] = grid_size
        self.__grid: list[pygame.Rect] = self.update_grid((0, 0))
        self.__cell_size = cell_size

        self.__bg_color: str = "black"
        self.__lines_color: str = "grey"
    
    def update_grid(self, starting_pos: tuple[int, int]) -> pygame.Rect:
        rects: list[pygame.Rect] = []
        for x in range(self.__grid_size[0]):
            for y in range(self.__grid_size[1]):
                rects.append(pygame.Rect(x * self.__cell_size, y * self.__cell_size, self.__cell_size, self.__cell_size))
        return rects

    def draw(self, grid: list[pygame.Rect], combined_grid: pygame.Rect) -> None:
        for cell in grid:
            pygame.draw.rect(self.__window, self.__lines_color, (cell.x + combined_grid.x, cell.y + combined_grid.y, self.__cell_size, self.__cell_size), 2)
    
    def main_loop(self) -> None:
        while True:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Clear the window
            self.__window.fill(self.__bg_color)

            # Draw
            self.draw(self.__grid, self.__grid[0].unionall(self.__grid))

            # Update
            self.__grid = self.update_grid(self.__grid[0].topleft)

            # Update the window
            pygame.display.update()
            self.__clock.tick(120)
    
    def run(self) -> None:
        self.main_loop()