def checkmate(board):
    if not isinstance(board, str):
        return
    list_board = board.splitlines()
    # print(list_board)
    grid_board = []
    for line in list_board:
        grid_board.append(list(line)) # เปลี่ยน "R..." เป็น ['R', '.', '.', '.']
    # print(grid_board)
        
    king_pos = None #ตำแหน่งของking 
    enemy_pieces = [] #ตำแหน่งของศัตรู มีหลายตำแหน่ง
    
    for r,row in enumerate(grid_board):
        if len(row) != len(grid_board):
            print("Error: Board is not square")
            return
        for c,char in enumerate(row):
            if char not in "PBRQK":
                grid_board[r][c] = '.' #ถ้าไม่ใช่ตัวที่กำหนดให้เป็นจุด
            else:
                if char == 'K':
                    if king_pos is not None:
                        print("Error: Can only have one King")
                        return
                    king_pos = (r,c)
                else:
                    #เก็บทั้งชนิดและพิกัดไว้ใน list เดียวกัน
                    enemy_pieces.append((char, r, c))
    if king_pos is None:
        print("Error: King is missing")
        return         

    for piece, start_r, start_c in enemy_pieces:
        # กำหนดทิศทางการเดินของแต่ละตัว
        directions = []
        if piece == 'P':
            directions = [(-1, -1), (-1, 1)]
        elif piece == 'R': 
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        elif piece == 'B':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece == 'Q':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            cur_r, cur_c = start_r + dr, start_c + dc
            while 0 <= cur_r < len(grid_board) and 0 <= cur_c < len(grid_board):
                # ถ้าเจอ King 
                if (cur_r, cur_c) == king_pos:
                    print("Success")
                    return
                if grid_board[cur_r][cur_c] != '.':
                    break
                if piece == 'P':
                    break
                # ไปช่องต่อไป
                cur_r += dr
                cur_c += dc
    print("Fail")
    # print(grid_board)
    # print(king_pos)
    # print(enemy_pieces)