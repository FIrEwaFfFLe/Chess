from pygame import *

import AI
import game


class SP(sprite.Sprite):
    def __init__(self, path, pos_x, pos_y):
        super().__init__()
        self.image = image.load(path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x + u // 2, pos_y + u // 2]

    def update(self, path, pos_x, pos_y):
        self.image = image.load(path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x + u // 2, pos_y + u // 2]



init()
u = 96
start = display.set_mode((8 * u, 8 * u))
display.set_caption("CHESS")
qwa = True
FPS = 100
play = 0
turn = True

start.fill((0, 0, 0))
# GRID______________________
for y in range(8):
    for x in range(8):
        col = (138, 201, 119)
        if (y + x) % 2 == 0:
            col = (255, 255, 255)
        draw.rect(start, col, Rect(x * u, y * u, u, u))

ai = int(input())
if ai:
    play = int(input())
# Sprites
# w_king = SP("sprites/w_king.png", 0, 0)
move_list = []
fig = []
qwerty = ["-", "w_king", "w_queen", "w_rook", "w_bishop", "w_knight", "w_pawn", "b_king", "b_queen", "b_rook",
          "b_bishop", "b_knight", "b_pawn"]
pie = []
if (not ai) or play == 0:
    for y in range(8):
        for x in range(8):
            if game.board[y][x] != 0:
                pie.append(SP("sprites/" + qwerty[game.board[y][x]] + ".png", x * u, y * u))
else:
    for y in range(8):
        for x in range(8):
            if game.board[y][x] != 0:
                pie.append(SP("sprites/" + qwerty[game.board[y][x]] + ".png", (7 - x) * u, (7 - y) * u))

sprite_group = sprite.Group()
for i in range(len(pie)):
    sprite_group.add(pie[i])

# Sprites___________________
sprite_group.draw(start)
display.update()


def main():
    global qwa, pos_x, pos_y, w_king, move_list, fig, turn
    circles = []
    rty = True
    moves = game.moves(turn)
    if turn == play and ai != 0 and game.event <= 1:
        move_list = []
        qwe = AI.main(game.board, game.last_first_move, game.castle, game.kings, turn, ai)
        game.move(qwe)
        fig = []
        turn = not turn
    else:
        while rty:
            for q in event.get():
                if q.type == QUIT:
                    qwa = False
                    rty = False
                    break
                elif q.type == MOUSEBUTTONDOWN:
                    rty = False
                    pos = mouse.get_pos()
                    if not turn:
                        pos = [8 * u - 1 - pos[0], 8 * u - 1 - pos[1]]
                    if len(move_list) != 0 and (pos[1] // u, pos[0] // u) in move_list:
                        game.move([fig, [pos[1] // u, pos[0] // u]])
                        move_list = []
                        fig = []
                        turn = not turn
                    else:
                        move_list = moves[pos[1] // u][pos[0] // u]
                        fig = [pos[1] // u, pos[0] // u]
                        for i in move_list:
                            if turn:
                                asdfgh = (i[1] * u + u // 2, i[0] * u + u // 2)
                            else:
                                asdfgh = (8 * u - 1 - i[1] * u - u // 2, 8 * u - 1 - i[0] * u - u // 2)
                            if game.board[i[0]][i[1]] == 0:
                                circles.append([asdfgh, True])
                            else:
                                circles.append([asdfgh, False])
    # GET_BOARD________________
    cnt = 0
    # game.printy()
    if ((not ai) and turn) or (ai and not play):
        for y in range(8):
            for x in range(8):
                if game.board[y][x] != 0:
                    pie[cnt].update("Chess-main/sprites/" + qwerty[game.board[y][x]] + ".png", x * u, y * u)
                    cnt += 1
    else:
        for y in range(8):
            for x in range(8):
                if game.board[y][x] != 0:
                    pie[cnt].update("Chess-main/sprites/" + qwerty[game.board[y][x]] + ".png", (7 - x) * u, (7 - y) * u)
                    cnt += 1
    for i in range(cnt, len(pie)):
        sprite_group.remove(pie[i])

    # FILL_____________________
    start.fill((0, 0, 0))
    # GRID______________________
    for y in range(8):
        for x in range(8):
            col = (138, 201, 119)
            if (y + x) % 2 == 0:
                col = (255, 255, 255)
            draw.rect(start, col, Rect(x * u, y * u, u, u))
    # Sprites___________________
    sprite_group.draw(start)
    for i in circles:
        if i[1]:
            draw.circle(start, (255, 255, 150), i[0], 17, 100)
        else:
            draw.circle(start, (255, 255, 170), i[0], u // 2, 7)
        # draw.circle(start, (255, 255, 50), i, 16, 1)
    display.update()


if __name__ == "__main__":
    clock = time.Clock()
    while qwa:
        clock.tick(FPS)
        main()
