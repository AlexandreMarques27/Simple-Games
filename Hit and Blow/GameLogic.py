import random
from Interface import draw_board
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from pygame import time


class Game:
    def __init__(self):
        self.turn = 1
        self.max_turns = 8
        self.num_colors = 4
        self.colors = ['red', 'blue', 'green', 'yellow', 'purple', 'white']
        self.combination_length = 4
        self.combination = self.generate_combination()
        self.board = self.create_board()

    def generate_combination(self):

        combination = []
        while len(combination) < self.combination_length:
            color_index = random.randint(1, self.num_colors)
            if color_index not in combination:
                combination.append(color_index)
        return combination

    def create_board(self):
        board = []
        for i in range(self.combination_length):
            board.append([0] * self.max_turns)
        return board

    def make_guess(self, color, position):
        clear = True
        for i in range(self.combination_length):
            if self.board[i][self.turn - 1] == color and i != position:
                clear = False
        if clear:
            self.board[position][self.turn - 1] = color

    def check_guess(self):
        result = []
        for i in range(self.combination_length):
            if self.board[i][self.turn-1] == self.combination[i]:
                result.append('Correct')
            elif self.board[i][self.turn-1] in self.combination:
                result.append('Almost')
            else:
                result.append('Incorrect')
        return result

    def print_board(self):
        for i in range(self.combination_length):
            print(self.board[i])
        print()

    def correct_guess(self, guess):
        for g in guess:
            if g != 'Correct':
                return False
        return True

    def game_over(self, guess):
        if self.turn == self.max_turns and not self.correct_guess(guess):
            return True
        if self.correct_guess(guess):
            return True
        return False

    def play_game(self, game):
        pygame.init()
        pygame.font.init()
        font = pygame.font.Font(None, 30)

        max_num = max(game.max_turns +1, game.num_colors)
        screen_width = (max_num) * 100  # columns * 100
        screen_height = (game.combination_length + 2) * 100  # rows * 100
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Mastermind Game")
        clock = pygame.time.Clock()
        offset = (screen.get_width() - (self.max_turns + 1) * 100) // 2

        selected_color = None
        draw_board(screen, game.board, game.combination, game.turn, selected_color)
        text = font.render(f"selected: None", True, (255, 255, 255))
        screen.blit(text, (self.max_turns * 100 + offset - 80, (self.combination_length + 2) * 100 + offset - 60))
        while game.turn <= game.max_turns:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    col = (mouse_pos[0] - offset) // 100
                    row = (mouse_pos[1] - offset) // 100
                    row = row - 1
                    if row == game.combination_length and col in range(game.max_turns):
                        if selected_color is None:
                            selected_color = col + 1
                            screen.fill((150, 150, 150))
                            draw_board(screen, game.board, game.combination, game.turn, selected_color)
                            text = font.render(f"selected: {self.colors[selected_color-1]}", True, (255, 255, 255))
                            screen.blit(text, (self.max_turns * 100 + offset - 80, (self.combination_length + 2) * 100 + offset - 60))
                        elif selected_color == col + 1:
                            selected_color = None
                            screen.fill((150, 150, 150))
                            draw_board(screen, game.board, game.combination, game.turn, selected_color)
                            text = font.render("selected: None", True, (255, 255, 255))
                            screen.blit(text, (self.max_turns * 100 + offset - 80, (self.combination_length + 2) * 100 + offset - 60))
                    elif row in range(game.combination_length) and col == game.turn-1:
                        if selected_color is not None:
                            game.make_guess(selected_color, row)
                            selected_color = None
                            screen.fill((150, 150, 150))
                            draw_board(screen, game.board, game.combination, game.turn, selected_color)
                            text = font.render(f"selected: None", True, (255, 255, 255))
                            screen.blit(text, (self.max_turns * 100 + offset - 80, (self.combination_length + 2) * 100 + offset - 60))

                            result = game.check_guess()

                            if game.game_over(result):
                                draw_board(screen, game.board, game.combination, game.turn+1, selected_color)
                                font = pygame.font.Font(None, 36)
                                if game.correct_guess(result):
                                    text = font.render("Game Over, you won", True, (0, 0, 0))
                                    text_rect = text.get_rect(center=(350, 350))
                                    screen.blit(text, text_rect)
                                    pygame.display.flip()
                                    time.wait(5000)
                                    pygame.quit()
                                    quit()
                                else:
                                    text = font.render("Game Over, you lost", True, (0, 0, 0))
                                    text_rect = text.get_rect(center=(350, 350))
                                    screen.blit(text, text_rect)
                                    pygame.display.flip()
                                    time.wait(5000)
                                    pygame.quit()
                                    quit()

                            pass_turn = True
                            for i in range(self.combination_length):
                                if game.board[i][game.turn-1] == 0:
                                    pass_turn = False

                            if pass_turn is True:
                                game.turn += 1
                                draw_board(screen, game.board, game.combination, game.turn, selected_color)
                                text = font.render("selected: None", True, (255, 255, 255))
                                screen.blit(text, (
                                self.max_turns * 100 + offset - 80, (self.combination_length + 2) * 100 + offset - 60))

            pygame.display.flip()
            clock.tick(30)  # Adjust the frame rate as needed
