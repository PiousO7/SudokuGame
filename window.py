import pygame
import requests

RED = "#ff0000"
WHITE = "#ffffff"
BLACK = "#000000"
GREEN = "#A4DE02"
START_POINT = (0, 0, 0)


class MainWindow:
    def __init__(self):
        pygame.init()
        # SCREEN
        self.screen = pygame.display.set_mode((550, 550))
        pygame.display.set_caption("Sudoku Game")
        self.screen.fill(WHITE)

        # FOR SETTING UP GRID
        self.constant_line_value = 50
        self.endpoint = 450

        # FONT
        self.font = pygame.font.SysFont('Comic Sans Ms', 30)

        # RANDOM SUDOKU GRID
        self.config = {"difficulty": "easy"}
        self.response = requests.get(url='https://sugoku.herokuapp.com/board?difficulty=easy')
        self.board = self.response.json()["board"]

        # SOLUTION
        self.board_solved = self.response.json()["board"]

        # TIMER
        self.clock = pygame.time.Clock()
        self.start_time = None

    # SETTING MAIN GRID THAT RUNS FOREVER
    def main_grid(self):
        for i in range(0, 10):
            if i % 3 == 0:
                pygame.draw.line(self.screen, START_POINT, (45 + 45 * i, self.constant_line_value),
                                 (45 + 45 * i, self.endpoint), 4)
                pygame.draw.line(self.screen, START_POINT, (self.constant_line_value, 45 + 45 * i),
                                 (self.endpoint, 45 + 45 * i), 4)
            pygame.draw.line(self.screen, START_POINT, (45 + 45 * i, self.constant_line_value),
                             (45 + 45 * i, self.endpoint), 2)
            pygame.draw.line(self.screen, START_POINT, (self.constant_line_value, 45 + 45 * i),
                             (self.endpoint, 45 + 45 * i), 2)
            pygame.display.update()

        while True:
            # TIMER
            self.timer()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                # IF RIGHT CLICK PRESSED THAT BOARD GETS SOLVED
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    self.sudoku_board(grid=self.board_solved)

                # IF LEFT CLICKED PRESSED IT ALLOWS USER TO ENTER NUMBER
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    # print(pos)
                    # print((int(pos[0] / 45), int(pos[1] / 45)))
                    self.enter_num(pos)
            pygame.display.update()

    # SETS UP THE INITIAL GRID OR SOLVES THE ENTIRE GRID DEPENDING ON THE INPUT VALUE OF GRID
    def sudoku_board(self, grid):
        for i in range(0, 9):
            for j in range(0, 9):
                if 0 < int(grid[i][j]) < 10:
                    value = self.font.render(str(grid[i][j]), True, BLACK)
                    self.screen.blit(value, ((j + 1) * 45 + 15, (i + 1) * 45))
        pygame.display.update()

    # LET'S USER ENTER NUMBER BETWEEN 0 and 9
    def enter_num(self, position):
        j = int(position[0] / 45)
        i = int(position[1] / 45)
        # print(self.board[i - 1][j - 1])
        # print(self.board_solved[i - 1][j - 1])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    return
                if event.type == pygame.KEYDOWN:
                    if self.board[i - 1][j - 1] != 0:
                        return
                    # IF 0 IS PRESSED, IT CLEARS THE BOX
                    if event.key == 48:
                        pygame.draw.rect(self.screen, WHITE, pygame.Rect(j * 45 + 5, i * 45 + 5, 35, 35))
                        return
                    # LET'S USER ENTER NUMBER
                    if 0 < event.key - 48 < 10:
                        key_pressed = event.key - 48
                        pygame.draw.rect(self.screen, WHITE, pygame.Rect(j * 45 + 5, i * 45 + 5, 35, 35))

                        # CHECKS USER'S INPUT ON A PARTICULAR BOX AND MAKES IT GREEN IF RIGHT AND RED FOR WRONG
                        if key_pressed == self.board_solved[i - 1][j - 1]:
                            value = self.font.render(str(key_pressed), True, GREEN)
                            self.screen.blit(value, (j * 45 + 15, i * 45 + 3, 45, 45))
                        else:
                            pygame.draw.rect(self.screen, WHITE, pygame.Rect(30, 470, 150, 45))
                            value = self.font.render(str(key_pressed), True, RED)
                            self.screen.blit(value, (j * 45 + 15, i * 45 + 3, 45, 45))
                        return

            pygame.display.update()

    # CREATES A TIMER
    def timer(self):
        time_since_enter = pygame.time.get_ticks()
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(440, 470, 100, 100))
        message = f"Timer: {str(int(time_since_enter / 1000))}"
        self.screen.blit(self.font.render(message, True, BLACK), (350, 470))
        pygame.display.flip()
        self.clock.tick(60)
