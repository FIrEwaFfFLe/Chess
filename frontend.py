from time import sleep
from random import *
from pygame import *
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
turn = True

# Sprites
# w_king = SP("sprites/w_king.png", 0, 0)
move_list = []
fig = []
qwerty = ["-", "w_king", "w_queen", "w_rook", "w_bishop", "w_knight", "w_pawn", "b_king", "b_queen", "b_rook",
          "b_bishop", "b_knight", "b_pawn"]
pie = []
for y in range(8):
    for x in range(8):
        if game.board[y][x] != 0:
            pie.append(SP("sprites/" + qwerty[game.board[y][x]] + ".png", x * u, y * u))

sprite_group = sprite.Group()
for i in range(len(pie)):
    sprite_group.add(pie[i])
# sprite_group.add(w_king)

start.fill((0, 0, 0))
# GRID______________________
for y in range(8):
    for x in range(8):
        col = (198, 236, 186)
        if (y + x) % 2 == 0:
            col = (255, 255, 255)
        draw.rect(start, col, Rect(x * u, y * u, u, u))
# Sprites___________________
sprite_group.draw(start)
display.update()


def main():
    global qwa, pos_x, pos_y, w_king, move_list, fig, turn
    moves = game.moves(turn)
    circles = []
    rty = True
    while rty:
        for q in event.get():
            if q.type == QUIT:
                qwa = False
                rty = False
                break
            elif q.type == MOUSEBUTTONDOWN:
                rty = False
                pos = mouse.get_pos()
                if len(move_list) != 0 and (pos[1] // u, pos[0] // u) in move_list:
                    game.move(fig, [pos[1] // u, pos[0] // u])
                    move_list = []
                    fig = []
                    turn = not turn
                else:
                    move_list = moves[pos[1] // u][pos[0] // u]
                    fig = [pos[1] // u, pos[0] // u]
                    for i in move_list:
                        if game.board[i[0]][i[1]] == 0:
                            circles.append([(i[1] * u + u // 2, i[0] * u + u // 2), True])
                        else:
                            circles.append([(i[1] * u + u // 2, i[0] * u + u // 2), False])
    # GET_BOARD________________
    cnt = 0
    # game.printy()
    for y in range(8):
        for x in range(8):
            if game.board[y][x] != 0:
                #print(cnt, game.board[y][x])
                pie[cnt].update("sprites/" + qwerty[game.board[y][x]] + ".png", x * u, y * u)
                cnt += 1
    for i in range(cnt, len(pie)):
        sprite_group.remove(pie[i])

    # FILL_____________________
    start.fill((0, 0, 0))
    # GRID______________________
    for y in range(8):
        for x in range(8):
            col = (198, 236, 186)
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
