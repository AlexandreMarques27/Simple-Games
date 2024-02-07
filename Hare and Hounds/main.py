import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from pygame import time


class Game:
    def __init__(self):
        self.board = self.create_board()
        self.initialize_players()
        self.turn = 1

    def copy(self):
        new_state = Game()
        new_state.board = [row[:] for row in self.board]
        new_state.turn = self.turn
        return new_state

    def create_board(self):
        board = []
        for i in range(3):
            board.append([0] * 5)
        board[0][0] = -2
        board[0][4] = -2
        board[2][0] = -2
        board[2][4] = -2
        return board

    def initialize_players(self):
        self.board[0][1] = 1
        self.board[1][0] = 1
        self.board[2][1] = 1
        self.board[1][4] = -1

    def is_clear(self, i, j):
        return (0 <= i < 3 and 0 <= j < 5 and self.board[i][j] == 0)

    def get_legal_moves(self, player):
        legal_moves = []
        for i in range(3):
            for j in range(5):
                if player == self.board[i][j] == 1:
                    for n in range(-1, 2):
                        for m in range(2):
                            if (i, j) == (1, 1):
                                if self.is_clear(i, j+1):
                                    legal_moves.append(((i, j), (i, j+1)))
                                if self.is_clear(i+1, j):
                                    legal_moves.append(((i, j), (i+1, j)))
                                if self.is_clear(i-1, j):
                                    legal_moves.append(((i, j), (i-1, j)))
                            elif (i, j) == (0, 2):
                                if self.is_clear(i+1, j):
                                    legal_moves.append(((i, j), (i+1, j)))
                                if self.is_clear(i, j+1):
                                    legal_moves.append(((i, j), (i, j+1)))
                            elif (i, j) == (2, 2):
                                if self.is_clear(i-1, j):
                                    legal_moves.append(((i, j), (i-1, j)))
                                if self.is_clear(i, j+1):
                                    legal_moves.append(((i, j), (i, j+1)))
                            elif self.is_clear(i+n, j+m):
                                legal_moves.append(((i, j), (i+n, j+m)))
                if player == self.board[i][j] == -1:
                    for n in range(-1, 2):
                        for m in range(-1, 2):
                            if (i, j) == (1, 3) or (i, j) == (1, 1) or (i, j) == (0, 2) or (i, j) == (2, 2):
                                if self.is_clear(i, j-1):
                                    legal_moves.append(((i, j), (i, j-1)))
                                if self.is_clear(i+1, j):
                                    legal_moves.append(((i, j), (i+1, j)))
                                if self.is_clear(i-1, j):
                                    legal_moves.append(((i, j), (i-1, j)))
                                if self.is_clear(i, j+1):
                                    legal_moves.append(((i, j), (i, j+1)))
                            elif self.is_clear(i+n, j+m):
                                legal_moves.append(((i, j), (i+n, j+m)))
        return legal_moves

    def change_turn(self):
        self.turn *= -1

    def make_move(self, position, move):
        if self.board[position[0]][position[1]] == self.turn and (position, move) in self.get_legal_moves(self.turn):
            self.board[position[0]][position[1]] = 0
            self.board[move[0]][move[1]] = self.turn
            return True
        return False

    def get_position_hounds(self):
        positions = []
        for i in range(3):
            for j in range(5):
                if self.board[i][j] == 1:
                    positions.append((i, j))
        return positions

    def get_position_hare(self):
        for i in range(3):
            for j in range(5):
                if self.board[i][j] == -1:
                    return (i, j)

    def game_over(self):
        if len(self.get_legal_moves(-1)) == 0:
            return 1
        position_hare = self.get_position_hare()
        position_hounds = self.get_position_hounds()
        flag = True
        for i in range(3):
            if position_hounds[i][1] < position_hare[1]:
                flag = False
        if flag:
            return -1
        return 0

    def generate_successors(self, state, player):
        successors = []
        cols = []
        for move in state.get_legal_moves(player):
            new_state = state.copy()
            new_state.make_move(move[0], move[1])
            successors.append(new_state)
            cols.append((move[0], move[1]))
        return successors, cols

    def heuristic(self, player):
        hounds_move = len(self.get_legal_moves(1))
        hare_move = len(self.get_legal_moves(-1))
        hare_position = self.get_position_hare()
        if player == -1:
            return 2 * hare_move + (4 - hare_position[1])
        else:
            return -hare_move

    def minimax(self, state, depth, maximizing_player):

        if depth == 0 or state.game_over() != 0:
            if state.game_over() != 0:
                if state.game_over() == 1:
                    return None, -512
                elif state.game_over() == -1:
                    return None, 512
                else:
                    return None, 0
            else:
                return None, abs(state.heuristic(-1))
        if maximizing_player:
            col = None
            value = float('-inf')
            successors, cols = self.generate_successors(state, -1)
            for i, child in enumerate(successors):
                _, child_value = self.minimax(child, depth - 1, False)
                value, col = max((value, col), (child_value, cols[i]))
            return col, value
        else:
            col = None
            value = float('inf')
            successors, cols = self.generate_successors(state, 1)
            for i, child in enumerate(successors):
                _, child_value = self.minimax(child, depth - 1, True)
                value, col = min((value, col), (child_value, cols[i]))
            return col, value

    def play_game(self):
        pygame.init()
        pygame.font.init()
        font = pygame.font.Font(None, 30)

        screen_width = 8 * 100  # columns * 100
        screen_height = 5 * 100  # rows * 100
        screen = pygame.display.set_mode((screen_width, screen_height))
        screen.fill((255, 255, 255))
        pygame.display.flip()

        pygame.display.set_caption("Hare and Hounds")
        clock = pygame.time.Clock()
        interface = Interface()
        selected_piece = None
        interface.draw_lines(screen, game)
        interface.draw_board(screen, game, selected_piece, [])

        while game.game_over() == 0:
            if self.turn == -1:
                col, value = self.minimax(self, 5, True)
                self.make_move(col[0], col[1])
                self.change_turn()
                interface.draw_board(screen, game, self.board, selected_piece)
                continue
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    col = mouse_pos[0] // 150
                    row = mouse_pos[1] // 150
                    if 0 <= row < 3 and 0 <= col < 5:
                        if selected_piece is None:
                            if game.board[row][col] == game.turn:
                                selected_piece = (row, col)

                        elif selected_piece == (row, col):
                            selected_piece = None

                        else:
                            legal_actions = self.get_legal_moves(self.turn)
                            possible_moves = [pair[1] for pair in legal_actions if pair[0] == selected_piece]
                            if (row, col) in possible_moves:
                                self.make_move(selected_piece, (row, col))
                                # self.print_board()
                                selected_piece = None
                                self.change_turn()
                                break
            possible_moves = self.get_legal_moves(self.turn)
            possible_moves = [pair[1] for pair in possible_moves if pair[0] == selected_piece]
            interface.draw_board(screen, game, selected_piece, possible_moves)
            pygame.display.flip()
            clock.tick(30)  # Adjust the frame rate as needed
        pygame.time.wait(1000)


    def print_board(self):
        for i in range(3):
            if i % 2 != 0:
                print(self.board[i])
            else:
                print("  ", self.board[i][1:-1], " ")
        print()


class Interface:
    def draw_lines(self, screen, game):
        rows, cols = len(game.board), len(game.board[0])
        for row in range(rows):
            for col in range(cols):
                x = col * 150 + 100
                y = row * 150 + 50
                if (row, col) not in [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]:
                    for i, j in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1), (1, 2)]:
                        if 0 <= i < rows and 0 <= j < cols and (i, j) not in [(0, 0), (0, cols - 1), (rows - 1, 0),
                                                                              (rows - 1, cols - 1)]:
                            pygame.draw.line(screen, (0, 0, 0), (x, y), (j * 150 + 100, i * 150 + 50), 2)

                    if (row, col) == (1, 0):
                        pygame.draw.line(screen, (0, 0, 0), (x, y), ((-col + 1) * 150 + 100, (-row + 1) * 150 + 50), 2)
                    elif (row, col) == (2, 1):
                        pygame.draw.line(screen, (0, 0, 0), (x, y), ((col - 1) * 150 + 100, (row - 1) * 150 + 50), 2)

                    elif (row, col) == (1, 4):
                        pygame.draw.line(screen, (0, 0, 0), (x, y), ((col - 1) * 150 + 100, (row - 1) * 150 + 50), 2)
                    elif (row, col) == (2, 3):
                        pygame.draw.line(screen, (0, 0, 0), (x, y), ((col + 1) * 150 + 100, (row - 1) * 150 + 50), 2)


    def draw_board(self, screen, game, selected_piece=None, legal_moves = None ):
        rows, cols = len(game.board), len(game.board[0])
        pygame.font.init()

        for row in range(rows):
            for col in range(cols):
                x = col * 150 + 100
                y = row * 150 + 50
                if game.board[row][col] == 1:
                    pygame.draw.circle(screen, (255, 0, 0), (x, y), 40)
                elif game.board[row][col] == -1:
                    pygame.draw.circle(screen, (0, 0, 0), (x, y), 40)
                elif game.board[row][col] == 0:
                    pygame.draw.circle(screen, (100, 100, 100), (x, y), 40)
                if (row, col) == selected_piece:
                    pygame.draw.circle(screen, (0, 255, 0), (x, y), 40)
                if legal_moves is not None and (row, col) in legal_moves:
                    pygame.draw.circle(screen, (0, 0, 255), (x, y), 40)

        pygame.display.flip()


game = Game()
game.play_game()
