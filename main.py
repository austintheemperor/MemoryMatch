import pygame
import random
import tkinter as tk
from tkinter import simpledialog, messagebox

# --- config ---
def get_board_size():
    while True:
        w = simpledialog.askinteger("Board Width", "Enter width:", minvalue=1)
        h = simpledialog.askinteger("Board Height", "Enter height:", minvalue=1)

        if w is None or h is None:
            return None, None

        if (w * h) % 2 == 0:
            return w, h

        messagebox.showerror("Invalid Board", "Width × Height must be even.")

# REQUIRED for tkinter dialogs to work reliably
root = tk.Tk()
root.withdraw()

WIDTH, HEIGHT = get_board_size()

if WIDTH is None:
    exit()

TILE_SIZE = 100
MARGIN = 10

SCREEN_WIDTH = WIDTH * (TILE_SIZE + MARGIN) + MARGIN
SCREEN_HEIGHT = HEIGHT * (TILE_SIZE + MARGIN) + MARGIN

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Game")
font = pygame.font.SysFont(None, 48)

# --- board ---
num_pairs = (WIDTH * HEIGHT) // 2
values = list(range(1, num_pairs + 1)) * 2
random.shuffle(values)

board = []
index = 0
for r in range(HEIGHT):
    row = []
    for c in range(WIDTH):
        row.append(values[index])
        index += 1
    board.append(row)

revealed = [[False]*WIDTH for _ in range(HEIGHT)]

first_pick = None
second_pick = None
lock = False

# --- draw ---
def draw():
    screen.fill((30, 30, 30))

    for r in range(HEIGHT):
        for c in range(WIDTH):
            x = c * (TILE_SIZE + MARGIN) + MARGIN
            y = r * (TILE_SIZE + MARGIN) + MARGIN

            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

            if revealed[r][c]:
                pygame.draw.rect(screen, (200, 200, 200), rect)
                text = font.render(str(board[r][c]), True, (0, 0, 0))
                screen.blit(text, text.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, (70, 130, 180), rect)

    pygame.display.flip()

# --- tile lookup ---
def get_tile(pos):
    mx, my = pos
    for r in range(HEIGHT):
        for c in range(WIDTH):
            x = c * (TILE_SIZE + MARGIN) + MARGIN
            y = r * (TILE_SIZE + MARGIN) + MARGIN
            if pygame.Rect(x, y, TILE_SIZE, TILE_SIZE).collidepoint(mx, my):
                return r, c
    return None

# --- game loop ---
running = True
clock = pygame.time.Clock()

while running:
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not lock:
            tile = get_tile(event.pos)
            if not tile:
                continue

            r, c = tile

            if revealed[r][c]:
                continue

            revealed[r][c] = True

            if first_pick is None:
                first_pick = (r, c)
            else:
                r1, c1 = first_pick
                r2, c2 = r, c

                if board[r1][c1] != board[r2][c2]:
                    second_pick = (r1, c1, r2, c2)
                    lock = True
                    pygame.time.set_timer(pygame.USEREVENT, 800)
                else:
                    first_pick = None

        # FIXED TIMER HANDLING
        if event.type == pygame.USEREVENT:
            if second_pick:
                r1, c1, r2, c2 = second_pick

                revealed[r1][c1] = False
                revealed[r2][c2] = False

            first_pick = None
            second_pick = None
            lock = False
            pygame.time.set_timer(pygame.USEREVENT, 0)

    clock.tick(60)

pygame.quit()