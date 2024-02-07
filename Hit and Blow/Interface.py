import pygame

RED = (255, 0, 0)

BLUE = (0, 0, 255)

GREEN = (0, 255, 0)

YELLOW = (255, 255, 0)

PURPLE = (255, 0, 255)

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

CYAN = (150, 150, 150)

COLORS = [RED, BLUE, GREEN, YELLOW, PURPLE, WHITE]


def draw_board(screen, board, combination, turn, selected):
    rows, cols = len(board), len(board[0])
    offset = (screen.get_width() - (cols+1) * 100) // 2
    screen.fill(CYAN)
    pygame.font.init()  # Initialize the font module
    font_size = 36

    for row in range(rows):
        for col in range(cols):
            x = col * 100 + 50 + offset
            y = row * 100 + 150 + offset

            # Draw the label
            label_text = f"{col+1}"
            font = pygame.font.Font(None, font_size)
            label_surface = font.render(label_text, True, BLACK)
            label_rect = label_surface.get_rect(center=(x, 100 + offset - 40))

            # Draw the label below the circle
            screen.blit(label_surface, label_rect)

            # Draw the board circles
            pygame.draw.circle(screen, BLACK, (x, y), 40)

            # Draw pieces
            if board[row][col] > 0:
                pygame.draw.circle(screen, COLORS[board[row][col] - 1], (x, y), 40)

            if row == rows - 1:
                if col < 6:
                    pygame.draw.circle(screen, COLORS[col], (x, y+100), 40)

            if col == cols - 1:
                pygame.draw.circle(screen, BLACK, (x + 100, y), 40, 5)
                for t in range(turn - 1):
                    if combination[row] == board[row][t]:
                        pygame.draw.circle(screen, COLORS[combination[row] - 1], (x + 100, y),
                                           40)

    '''
    for i in range(rows):
        pygame.draw.circle(screen, BLACK, (screen.get_width() - 50, i * 100 + 150), 40, 5)
        for t in range(turn-1):
            if combination[i] == board[i][t]:
                pygame.draw.circle(screen, COLORS[combination[i] - 1], (screen.get_width() - 50, i * 100 + 150), 40)
    for i, color in enumerate(COLORS):
        pygame.draw.circle(screen, color, (i * 100 + 150, screen.get_height() - 50), 40)
    '''
    # Display the current turn
    font = pygame.font.Font(None, 36)
    text = font.render(f'Turn {turn}', True, (255, 255, 255))
    screen.blit(text, (10, 10))


    pygame.display.flip()
