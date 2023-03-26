from copy import deepcopy


def ev():
    moveswhite = moves(1)
    movesblack = moves(0)
    if len(moveswhite) == 0:
        return -40
    elif len(movesblack) == 0:
        return 40
    qwe = 0
    qwerty = [0, 0, 9, 5, 3, 3, 1, 0, -9, -5, -3, -3, -1]
    for y in range(8):
        for x in range(8):
            qwe += qwerty[board[y][x]]
    return qwe


def go(n, t):
    global board, last_first_move, castle, kings
    if n == 0:
        return ev()
    boardk = deepcopy(board)
    last_first_movek = deepcopy(last_first_move)
    castlek = deepcopy(castle)
    kingsk = deepcopy(kings)
    mo = moves(t)
    cost = 0
    if n % 2 == 1 and t:
        cost = -45
    elif n % 2 == 1 and not t:
        cost = 45
    for i in mo:
        board = deepcopy(boardk)
        last_first_move = deepcopy(last_first_movek)
        castle = deepcopy(castlek)
        kings = deepcopy(kingsk)
        if len(i) == 2:
            move([i[0], i[1]])
        else:
            move([i[0], i[1], i[2]])
        if n % 2 == 0:
            cost += go(n - 1, 1 - t)
        else:
            dyuf = go(n - 1, 1 - t)
            if t and dyuf > cost:
                cost = dyuf
            elif not t and dyuf < cost:
                cost = dyuf
    if len(mo) == 0:
        return -40 + (1 - t) * 80
    elif n % 2 == 0:
        return cost / len(mo)
    else:
        return cost


def main(board1, last_first_move1, castle1, kings1, turn1, depth):
    global board, last_first_move, castle, kings
    board = board1
    last_first_move = last_first_move1
    castle = castle1
    kings = kings1
    # ________________________________________________
    boardk = deepcopy(board)
    last_first_movek = deepcopy(last_first_move)
    castlek = deepcopy(castle)
    kingsk = deepcopy(kings)
    mo = moves(turn1)
    costs = []
    for i in mo:
        board = deepcopy(boardk)
        last_first_move = deepcopy(last_first_movek)
        castle = deepcopy(castlek)
        kings = deepcopy(kingsk)
        if len(i) == 2:
            move([i[0], i[1]])
        else:
            move([i[0], i[1], i[2]])
        costs.append(go(2 * depth - 1, 1 - turn1))
    if turn1:
        return mo[costs.index(max(costs))]
    else:
        return mo[costs.index(min(costs))]


def check(q):
    # // ans = []
    ans = False
    # pieces = [knigt, bishop, rook, queen]
    pieces = [5, 4, 3, 2]
    yk, xk = 0, 0
    if q:
        pieces = [11, 10, 9, 8]
        yk, xk = kings[0][0], kings[0][1]
        # pawns
        if yk != 0 and (xk != 0 and board[yk - 1][xk - 1] == 12):
            # // ans.append([12, yk - 1, xk - 1])
            ans = True
        if yk != 0 and (xk != 7 and board[yk - 1][xk + 1] == 12):
            # // ans.append([12, yk - 1, xk + 1])
            ans = True
    else:
        yk, xk = kings[1][0], kings[1][1]
        # pawns
        if yk != 7 and (xk != 0 and board[yk + 1][xk - 1] == 6):
            # // ans.append([6, yk + 1, xk - 1])
            ans = True
        if yk != 7 and (xk != 7 and board[yk + 1][xk + 1] == 6):
            # // ans.append([6, yk + 1, xk + 1])
            ans = True
    # knights
    knigt = [[2, 2, -2, -2, 1, 1, -1, -1], [1, -1, 1, -1, 2, -2, 2, -2]]
    for i in range(8):
        y = yk + knigt[0][i]
        x = xk + knigt[1][i]
        if 0 <= y <= 7 and 0 <= x <= 7 and board[y][x] == pieces[0]:
            # // ans.append([pieces[0], y, x])
            ans = True
    # diagonal (queen and bishop)
    # >_
    for i in range(7 - max(yk, xk)):
        y = yk + i + 1
        x = xk + i + 1
        if board[y][x] != 0:
            if board[y][x] == pieces[1] or board[y][x] == pieces[3]:
                # // ans.append([board[y][x], y, x])
                ans = True
            break
    # >^
    for i in range(min(7 - xk, yk)):
        y = yk - i - 1
        x = xk + i + 1
        if board[y][x] != 0:
            if board[y][x] == pieces[1] or board[y][x] == pieces[3]:
                # // ans.append([board[y][x], y, x])
                ans = True
            break
    # <_
    for i in range(min(xk, 7 - yk)):
        y = yk + i + 1
        x = xk - i - 1
        if board[y][x] != 0:
            if board[y][x] == pieces[1] or board[y][x] == pieces[3]:
                # // ans.append([board[y][x], y, x])
                ans = True
            break
    # <^
    for i in range(min(yk, xk)):
        y = yk - i - 1
        x = xk - i - 1
        if board[y][x] != 0:
            if board[y][x] == pieces[1] or board[y][x] == pieces[3]:
                # // ans.append([board[y][x], y, x])
                ans = True
            break
    # straight line (rook and queen)
    # ^
    for i in range(yk):
        y = yk - i - 1
        x = xk
        if board[y][x] != 0:
            if board[y][x] == pieces[2] or board[y][x] == pieces[3]:
                # // ans.append([board[y][x], y, x])
                ans = True
            break
    # _
    for i in range(7 - yk):
        y = yk + i + 1
        x = xk
        if board[y][x] != 0:
            if board[y][x] == pieces[2] or board[y][x] == pieces[3]:
                # // ans.append([board[y][x], y, x])
                ans = True
            break
    # <
    for i in range(xk):
        y = yk
        x = xk - i - 1
        if board[y][x] != 0:
            if board[y][x] == pieces[2] or board[y][x] == pieces[3]:
                # // ans.append([board[y][x], y, x])
                ans = True
            break
    # >
    for i in range(7 - xk):
        y = yk
        x = xk + i + 1
        if board[y][x] != 0:
            if board[y][x] == pieces[2] or board[y][x] == pieces[3]:
                # // ans.append([board[y][x], y, x])
                ans = True
            break
    # KING
    king = [[1, 1, 1, 0, 0, -1, -1, -1], [-1, 0, 1, 1, -1, -1, 0, 1]]
    for i in range(8):
        y = yk + king[0][i]
        x = xk + king[1][i]
        if 0 <= y <= 7 and 0 <= x <= 7 and board[y][x] == 1 + 6 * q:
            # // ans.append([pieces[0], y, x])
            ans = True
    return ans


def moves(turn):
    ans = []
    cnt = 0
    for y in range(8):
        for x in range(8):
            # if our piece
            if board[y][x] == 0 or (turn and board[y][x] >= 7) or (not turn and board[y][x] < 7):
                continue
            p = board[y][x]
            # king
            if p == 1 or p == 7:
                king = [[1, 1, 1, 0, 0, -1, -1, -1], [-1, 0, 1, 1, -1, -1, 0, 1]]
                for i in range(8):
                    yk, xk = y + king[0][i], x + king[1][i]
                    if 0 <= yk <= 7 and 0 <= xk <= 7 and ((turn and not (1 <= board[yk][xk] <= 6)) or (not turn and not (7 <= board[yk][xk] <= 12))):
                        kill = board[yk][xk]
                        board[yk][xk] = p
                        board[y][x] = 0
                        kings[1 - turn] = [yk, xk]
                        if not check(turn):
                            ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = kill
                        board[y][x] = p
                        kings[1 - turn] = [y, x]
            # DIAGONALS
            if p == 8 or p == 2 or p == 4 or p == 10:
                # >_
                for i in range(7 - max(y, x)):
                    yk = y + i + 1
                    xk = x + i + 1
                    kill = board[yk][xk]
                    if kill == 0:
                        board[yk][xk] = p
                        board[y][x] = 0
                        if not check(turn):
                            ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = kill
                        board[y][x] = p
                        continue
                    else:
                        if (turn and not (1 <= kill <= 6)) or (not turn and not (7 <= kill <= 12)):
                            board[yk][xk] = p
                            board[y][x] = 0
                            if not check(turn):
                                ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = kill
                            board[y][x] = p
                        break
                # >^
                for i in range(min(7 - x, y)):
                    yk = y - i - 1
                    xk = x + i + 1
                    kill = board[yk][xk]
                    if kill == 0:
                        board[yk][xk] = p
                        board[y][x] = 0
                        if not check(turn):
                            ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = kill
                        board[y][x] = p
                        continue
                    else:
                        if (turn and not (1 <= kill <= 6)) or (not turn and not (7 <= kill <= 12)):
                            board[yk][xk] = p
                            board[y][x] = 0
                            if not check(turn):
                                ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = kill
                            board[y][x] = p
                        break
                # <^
                for i in range(min(y, x)):
                    yk = y - i - 1
                    xk = x - i - 1
                    kill = board[yk][xk]
                    if kill == 0:
                        board[yk][xk] = p
                        board[y][x] = 0
                        if not check(turn):
                            ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = kill
                        board[y][x] = p
                        continue
                    else:
                        if (turn and not (1 <= kill <= 6)) or (not turn and not (7 <= kill <= 12)):
                            board[yk][xk] = p
                            board[y][x] = 0
                            if not check(turn):
                                ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = kill
                            board[y][x] = p
                        break
                # <_
                for i in range(min(x, 7 - y)):
                    yk = y + i + 1
                    xk = x - i - 1
                    kill = board[yk][xk]
                    if kill == 0:
                        board[yk][xk] = p
                        board[y][x] = 0
                        if not check(turn):
                            ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = kill
                        board[y][x] = p
                        continue
                    else:
                        if (turn and not (1 <= kill <= 6)) or (not turn and not (7 <= kill <= 12)):
                            board[yk][xk] = p
                            board[y][x] = 0
                            if not check(turn):
                                ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = kill
                            board[y][x] = p
                        break
            # STRAIGHT LINES
            if p == 2 or p == 8 or p == 3 or p == 9:
                # ^
                for i in range(y):
                    yk = y - i - 1
                    xk = x
                    kill = board[yk][xk]
                    if kill == 0:
                        board[yk][xk] = p
                        board[y][x] = 0
                        if not check(turn):
                            ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = kill
                        board[y][x] = p
                        continue
                    else:
                        if (turn and not (1 <= kill <= 6)) or (not turn and not (7 <= kill <= 12)):
                            board[yk][xk] = p
                            board[y][x] = 0
                            if not check(turn):
                                ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = kill
                            board[y][x] = p
                        break
                # _
                for i in range(7 - y):
                    yk = y + i + 1
                    xk = x
                    kill = board[yk][xk]
                    if kill == 0:
                        board[yk][xk] = p
                        board[y][x] = 0
                        if not check(turn):
                            ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = kill
                        board[y][x] = p
                        continue
                    else:
                        if (turn and not (1 <= kill <= 6)) or (not turn and not (7 <= kill <= 12)):
                            board[yk][xk] = p
                            board[y][x] = 0
                            if not check(turn):
                                ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = kill
                            board[y][x] = p
                        break
                # <
                for i in range(x):
                    yk = y
                    xk = x - i - 1
                    kill = board[yk][xk]
                    if kill == 0:
                        board[yk][xk] = p
                        board[y][x] = 0
                        if not check(turn):
                            ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = kill
                        board[y][x] = p
                        continue
                    else:
                        if (turn and not (1 <= kill <= 6)) or (not turn and not (7 <= kill <= 12)):
                            board[yk][xk] = p
                            board[y][x] = 0
                            if not check(turn):
                                ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = kill
                            board[y][x] = p
                        break
                # >
                for i in range(7 - x):
                    yk = y
                    xk = x + i + 1
                    kill = board[yk][xk]
                    if kill == 0:
                        board[yk][xk] = p
                        board[y][x] = 0
                        if not check(turn):
                            ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = kill
                        board[y][x] = p
                        continue
                    else:
                        if (turn and not (1 <= kill <= 6)) or (not turn and not (7 <= kill <= 12)):
                            board[yk][xk] = p
                            board[y][x] = 0
                            if not check(turn):
                                ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = kill
                            board[y][x] = p
                        break
            # KNIGHTS
            if p == 5 or p == 11:
                knight = [[1, 1, 2, 2, -1, -1, -2, -2], [2, -2, 1, -1, 2, -2, 1, -1]]
                for i in range(8):
                    yk, xk = y + knight[0][i], x + knight[1][i]
                    if 0 <= yk <= 7 and 0 <= xk <= 7 and ((turn and not (1 <= board[yk][xk] <= 6)) or (not turn and not (7 <= board[yk][xk] <= 12))):
                        kill = board[yk][xk]
                        board[yk][xk] = p
                        board[y][x] = 0
                        if not check(turn):
                            ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = kill
                        board[y][x] = p
            # PAWNS
            if p == 6:
                yk, xk = y - 1, x
                if 0 <= yk <= 7 and 0 <= xk <= 7 and board[yk][xk] == 0:
                    board[yk][xk] = p
                    board[y][x] = 0
                    if not check(turn):
                        if yk == 0:
                            ans.append([(y, x), (yk, xk), 2])
                            ans.append([(y, x), (yk, xk), 3])
                            ans.append([(y, x), (yk, xk), 4])
                            ans.append([(y, x), (yk, xk), 5])
                        else:
                            ans.append([(y, x), (yk, xk)])
                        cnt += 1
                    board[yk][xk] = 0
                    board[y][x] = p
                if y == 6:
                    yk -= 1
                    if 0 <= yk <= 7 and 0 <= xk <= 7 and board[yk][xk] == 0 and board[yk + 1][xk] == 0:
                        board[yk][xk] = p
                        board[y][x] = 0
                        if not check(turn):
                            if yk == 0:
                                ans.append([(y, x), (yk, xk), 2])
                                ans.append([(y, x), (yk, xk), 3])
                                ans.append([(y, x), (yk, xk), 4])
                                ans.append([(y, x), (yk, xk), 5])
                            else:
                                ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = 0
                        board[y][x] = p
                yk, xk = y - 1, x - 1
                if 0 <= yk <= 7 and 0 <= xk <= 7 and 7 <= board[yk][xk] <= 12:
                    kill = board[yk][xk]
                    board[yk][xk] = p
                    board[y][x] = 0
                    if not check(turn):
                        if yk == 0:
                            ans.append([(y, x), (yk, xk), 2])
                            ans.append([(y, x), (yk, xk), 3])
                            ans.append([(y, x), (yk, xk), 4])
                            ans.append([(y, x), (yk, xk), 5])
                        else:
                            ans.append([(y, x), (yk, xk)])
                        cnt += 1
                    board[yk][xk] = kill
                    board[y][x] = p
                yk, xk = y - 1, x + 1
                if 0 <= yk <= 7 and 0 <= xk <= 7 and 7 <= board[yk][xk] <= 12:
                    kill = board[yk][xk]
                    board[yk][xk] = p
                    board[y][x] = 0
                    if not check(turn):
                        if yk == 0:
                            ans.append([(y, x), (yk, xk), 2])
                            ans.append([(y, x), (yk, xk), 3])
                            ans.append([(y, x), (yk, xk), 4])
                            ans.append([(y, x), (yk, xk), 5])
                        else:
                            ans.append([(y, x), (yk, xk)])
                        cnt += 1
                    board[yk][xk] = kill
                    board[y][x] = p
                if y == 3:
                    if x != 0 and last_first_move[turn][x - 1]:
                        yk, xk = y - 1, x - 1
                        if 0 <= yk <= 7 and 0 <= xk <= 7:
                            board[yk][xk] = p
                            board[y][x] = 0
                            board[y][x - 1] = 0
                            if not check(turn):
                                if yk == 0:
                                    ans.append([(y, x), (yk, xk), 2])
                                    ans.append([(y, x), (yk, xk), 3])
                                    ans.append([(y, x), (yk, xk), 4])
                                    ans.append([(y, x), (yk, xk), 5])
                                else:
                                    ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = 0
                            board[y][x] = p
                            board[y][x - 1] = 12
                    if x != 7 and last_first_move[turn][x + 1]:
                        yk, xk = y - 1, x + 1
                        if 0 <= yk <= 7 and 0 <= xk <= 7:
                            board[yk][xk] = p
                            board[y][x] = 0
                            board[y][x + 1] = 0
                            if not check(turn):
                                if yk == 0:
                                    ans.append([(y, x), (yk, xk), 2])
                                    ans.append([(y, x), (yk, xk), 3])
                                    ans.append([(y, x), (yk, xk), 4])
                                    ans.append([(y, x), (yk, xk), 5])
                                else:
                                    ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = 0
                            board[y][x] = p
                            board[y][x + 1] = 12

            # PAWNS BLACK
            if p == 12:
                yk, xk = y + 1, x
                if 0 <= yk <= 7 and 0 <= xk <= 7 and board[yk][xk] == 0:
                    board[yk][xk] = p
                    board[y][x] = 0
                    if not check(turn):
                        if yk == 7:
                            ans.append([(y, x), (yk, xk), 2])
                            ans.append([(y, x), (yk, xk), 3])
                            ans.append([(y, x), (yk, xk), 4])
                            ans.append([(y, x), (yk, xk), 5])
                        else:
                            ans.append([(y, x), (yk, xk)])
                        cnt += 1
                    board[yk][xk] = 0
                    board[y][x] = p
                if y == 1:
                    yk += 1
                    if 0 <= yk <= 7 and 0 <= xk <= 7 and board[yk][xk] == 0 and board[yk - 1][xk] == 0:
                        board[yk][xk] = p
                        board[y][x] = 0
                        if not check(turn):
                            if yk == 7:
                                ans.append([(y, x), (yk, xk), 2])
                                ans.append([(y, x), (yk, xk), 3])
                                ans.append([(y, x), (yk, xk), 4])
                                ans.append([(y, x), (yk, xk), 5])
                            else:
                                ans.append([(y, x), (yk, xk)])
                            cnt += 1
                        board[yk][xk] = 0
                        board[y][x] = p
                yk, xk = y + 1, x + 1
                if 0 <= yk <= 7 and 0 <= xk <= 7 and 1 <= board[yk][xk] <= 6:
                    kill = board[yk][xk]
                    board[yk][xk] = p
                    board[y][x] = 0
                    if not check(turn):
                        if yk == 7:
                            ans.append([(y, x), (yk, xk), 2])
                            ans.append([(y, x), (yk, xk), 3])
                            ans.append([(y, x), (yk, xk), 4])
                            ans.append([(y, x), (yk, xk), 5])
                        else:
                            ans.append([(y, x), (yk, xk)])
                        cnt += 1
                    board[yk][xk] = kill
                    board[y][x] = p
                yk, xk = y + 1, x - 1
                if 0 <= yk <= 7 and 0 <= xk <= 7 and 1 <= board[yk][xk] <= 6:
                    kill = board[yk][xk]
                    board[yk][xk] = p
                    board[y][x] = 0
                    if not check(turn):
                        if yk == 7:
                            ans.append([(y, x), (yk, xk), 2])
                            ans.append([(y, x), (yk, xk), 3])
                            ans.append([(y, x), (yk, xk), 4])
                            ans.append([(y, x), (yk, xk), 5])
                        else:
                            ans.append([(y, x), (yk, xk)])
                        cnt += 1
                    board[yk][xk] = kill
                    board[y][x] = p
                if y == 4:
                    if x != 0 and last_first_move[turn][x - 1]:
                        yk, xk = y + 1, x - 1
                        if 0 <= yk <= 7 and 0 <= xk <= 7:
                            board[yk][xk] = p
                            board[y][x] = 0
                            board[y][x - 1] = 0
                            if not check(turn):
                                if yk == 7:
                                    ans.append([(y, x), (yk, xk), 2])
                                    ans.append([(y, x), (yk, xk), 3])
                                    ans.append([(y, x), (yk, xk), 4])
                                    ans.append([(y, x), (yk, xk), 5])
                                else:
                                    ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = 0
                            board[y][x] = p
                            board[y][x - 1] = 6
                    if x != 7 and last_first_move[turn][x + 1]:
                        yk, xk = y + 1, x + 1
                        if 0 <= yk <= 7 and 0 <= xk <= 7:
                            board[yk][xk] = p
                            board[y][x] = 0
                            board[y][x + 1] = 0
                            if not check(turn):
                                if yk == 7:
                                    ans.append([(y, x), (yk, xk), 2])
                                    ans.append([(y, x), (yk, xk), 3])
                                    ans.append([(y, x), (yk, xk), 4])
                                    ans.append([(y, x), (yk, xk), 5])
                                else:
                                    ans.append([(y, x), (yk, xk)])
                                cnt += 1
                            board[yk][xk] = 0
                            board[y][x] = p
                            board[y][x + 1] = 6
            # CASTLE
            if p == 1 and turn and castle[0][1]:
                if castle[0][0] and board[7][1] == 0 and board[7][2] == 0 and board[7][3] == 0 and not check(True):
                    yk, xk = y, x - 1
                    board[yk][xk] = p
                    board[y][x] = 0
                    kings[1 - turn] = [yk, xk]
                    if not check(turn):
                        ykk, xkk = yk, xk - 1
                        board[ykk][xkk] = p
                        board[yk][xk] = 0
                        kings[1 - turn] = [ykk, xkk]
                        if not check(turn):
                            ans.append([(y, x), (ykk, xkk)])
                            cnt += 1
                        board[ykk][xkk] = 0
                        board[yk][xk] = p
                        kings[1 - turn] = [yk, xk]
                    board[yk][xk] = 0
                    board[y][x] = p
                    kings[1 - turn] = [y, x]
                if castle[0][2] and board[7][6] == 0 and board[7][5] == 0 and not check(True):
                    yk, xk = y, x + 1
                    board[yk][xk] = p
                    kings[1 - turn] = [yk, xk]
                    board[y][x] = 0
                    if not check(turn):
                        ykk, xkk = yk, xk + 1
                        board[ykk][xkk] = p
                        kings[1 - turn] = [ykk, xkk]
                        board[yk][xk] = 0
                        if not check(turn):
                            ans.append([(y, x), (ykk, xkk)])
                            cnt += 1
                        board[ykk][xkk] = 0
                        kings[1 - turn] = [yk, xk]
                        board[yk][xk] = p
                    board[yk][xk] = 0
                    kings[1 - turn] = [y, x]
                    board[y][x] = p

            if p == 7 and not turn and castle[1][1]:
                if castle[1][0] and board[0][1] == 0 and board[0][2] == 0 and board[0][3] == 0 and not check(True):
                    yk, xk = y, x - 1
                    board[yk][xk] = p
                    board[y][x] = 0
                    kings[1 - turn] = [yk, xk]
                    if not check(turn):
                        ykk, xkk = yk, xk - 1
                        board[ykk][xkk] = p
                        board[yk][xk] = 0
                        kings[1 - turn] = [ykk, xkk]
                        if not check(turn):
                            ans.append([(y, x), (ykk, xkk)])
                            cnt += 1
                        board[ykk][xkk] = 0
                        board[yk][xk] = p
                        kings[1 - turn] = [yk, xk]
                    board[yk][xk] = 0
                    board[y][x] = p
                    kings[1 - turn] = [y, x]
                if castle[1][2] and board[0][6] == 0 and board[0][5] == 0 and not check(True):
                    yk, xk = y, x + 1
                    board[yk][xk] = p
                    kings[1 - turn] = [yk, xk]
                    board[y][x] = 0
                    if not check(turn):
                        ykk, xkk = yk, xk + 1
                        board[ykk][xkk] = p
                        kings[1 - turn] = [ykk, xkk]
                        board[yk][xk] = 0
                        if not check(turn):
                            ans.append([(y, x), (ykk, xkk)])
                            cnt += 1
                        board[ykk][xkk] = 0
                        kings[1 - turn] = [yk, xk]
                        board[yk][xk] = p
                    board[yk][xk] = 0
                    kings[1 - turn] = [y, x]
                    board[y][x] = p
    return ans


def move(asd):
    y1, x1 = asd[0][0], asd[0][1]
    y2, x2 = asd[1][0], asd[1][1]
    p = board[y1][x1]
    prom = -1
    if 7 <= p <= 12:
        last_first_move[1] = [False] * 8
    else:
        last_first_move[0] = [False] * 8
    if p == 6 and y1 - y2 == 2:
        last_first_move[0][x1] = True
    elif p == 6 and y2 == 0:
        prom = asd[2]
    elif p == 6 and y1 == 3 and y2 == 2 and x2 - x1 != 0 and board[y2][x2] == 0:
        board[y2 + 1][x2] = 0
    elif p == 12 and y2 - y1 == 2:
        last_first_move[1][x1] = True
    elif p == 12 and y2 == 7:
        prom = asd[2]
    elif p == 12 and y1 == 4 and y2 == 5 and x2 - x1 != 0 and board[y2][x2] == 0:
        board[y2 - 1][x2] = 0

    board[y2][x2] = p
    if prom != -1:
        board[y2][x2] = prom
    board[y1][x1] = 0
    if p == 1:
        kings[0] = [y2, x2]
        castle[0][1] = False
        if y1 == 7 and x1 - x2 == 2:
            board[7][0] = 0
            board[7][3] = 3
        elif y1 == 7 and x2 - x1 == 2:
            board[7][7] = 0
            board[7][5] = 3
    elif p == 7:
        kings[1] = [y2, x2]
        castle[1][1] = False
        if y1 == 0 and x1 - x2 == 2:
            board[0][0] = 0
            board[0][3] = 9
        elif y1 == 0 and x2 - x1 == 2:
            board[0][7] = 0
            board[0][5] = 9
    elif p == 3 and [y1, x1] == [7, 0]:
        castle[0][0] = False
    elif p == 3 and [y1, x1] == [7, 7]:
        castle[0][2] = False
    elif p == 9 and [y1, x1] == [0, 0]:
        castle[1][0] = False
    elif p == 9 and [y1, x1] == [0, 7]:
        castle[1][2] = False


def printy(qwer):
    for i in range(8):
        for j in range(8):
            if j != 7:
                print(qwer[i][j], end=" ")
            else:
                print(qwer[i][j])


board = [[9, 11, 10, 8, 7, 10, 11, 9],
         [12, 12, 12, 12, 12, 12, 12, 12],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [6, 6, 6, 6, 6, 6, 6, 6],
         [3, 5, 4, 2, 1, 4, 5, 3]]
last_first_move = [[False] * 8, [False] * 8]
castle = [[True, True, True], [True, True, True]]
kings = [[7, 4], [0, 4]]

