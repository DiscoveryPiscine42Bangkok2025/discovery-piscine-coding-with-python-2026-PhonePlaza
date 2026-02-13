from checkmate import checkmate

# =============================================================================
#  Helper: เรียก checkmate แล้ว capture stdout เพื่อเทียบผลลัพธ์
# =============================================================================
import io, sys

def run(board):
    """คืนค่า string ที่ checkmate() print ออกมา (ตัดช่องว่างท้ายบรรทัด)"""
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    checkmate(board)
    sys.stdout = old
    return buf.getvalue().strip()

# =============================================================================
#  1. ตัวอย่างจากโจทย์ (Subject Examples)
# =============================================================================
def test_example1():
    """Example1 จากโจทย์: Rook โจมตี King → Success"""
    board = """\
R...
.K..
..P.
...."""
    assert run(board) == "Success", "Example1: Rook should check King"

def test_example2():
    """Example2 จากโจทย์: King อยู่คนเดียว ไม่มีใครโจมตี → Fail"""
    board = """\
..
.K"""
    assert run(board) == "Fail", "Example2: No enemy → Fail"

# =============================================================================
#  2. Pawn Tests  (โจมตีทแยงด้านบน 1 ช่อง)
# =============================================================================
def test_pawn_check_left_diagonal():
    """Pawn โจมตี King ทแยงซ้ายบน"""
    board = """\
....
.K..
..P.
...."""
    assert run(board) == "Success"

def test_pawn_check_right_diagonal():
    """Pawn โจมตี King ทแยงขวาบน"""
    board = """\
....
...K
..P.
...."""
    assert run(board) == "Success"

def test_pawn_no_check_same_column():
    """Pawn อยู่ตรงหน้า King → ไม่ check (Pawn จับตรงไม่ได้)"""
    board = """\
....
..K.
..P.
...."""
    assert run(board) == "Fail"

def test_pawn_no_check_behind():
    """Pawn อยู่ด้านหลัง King → ไม่ check"""
    board = """\
....
..P.
..K.
...."""
    assert run(board) == "Fail"  # Pawn โจมตีขึ้นบนเท่านั้น

def test_pawn_no_check_too_far():
    """Pawn ห่าง King 2 แถว → ไม่ check (Pawn เดิน 1 ช่องเท่านั้น)"""
    board = """\
K...
....
.P..
...."""
    assert run(board) == "Fail"

# =============================================================================
#  3. Rook Tests  (แนวตั้ง + แนวนอน, ถูก block ได้)
# =============================================================================
def test_rook_check_horizontal():
    """Rook เดินแนวนอนโจมตี King"""
    board = """\
....
R..K
....
...."""
    assert run(board) == "Success"

def test_rook_check_vertical():
    """Rook เดินแนวตั้งโจมตี King"""
    board = """\
.R..
....
....
.K.."""
    assert run(board) == "Success"

def test_rook_blocked_by_piece():
    """Rook ถูก Pawn บังทาง → ไม่ check"""
    board = """\
....
R.PK
....
...."""
    assert run(board) == "Fail"

def test_rook_no_check_diagonal():
    """Rook อยู่ทแยง King → ไม่ check"""
    board = """\
R...
....
..K.
...."""
    assert run(board) == "Fail"

# =============================================================================
#  4. Bishop Tests  (ทแยง, ถูก block ได้)
# =============================================================================
def test_bishop_check_diagonal():
    """Bishop โจมตี King ทแยง"""
    board = """\
B...
....
..K.
...."""
    assert run(board) == "Success"

def test_bishop_blocked():
    """Bishop ถูก Pawn บังทาง → ไม่ check"""
    board = """\
B...
.P..
..K.
...."""
    assert run(board) == "Fail"

def test_bishop_no_check_straight():
    """Bishop อยู่แนวตรง King → ไม่ check"""
    board = """\
.B..
....
.K..
...."""
    assert run(board) == "Fail"

# =============================================================================
#  5. Queen Tests  (ทั้งตรง + ทแยง, ถูก block ได้)
# =============================================================================
def test_queen_check_horizontal():
    """Queen โจมตีแนวนอน"""
    board = """\
....
Q..K
....
...."""
    assert run(board) == "Success"

def test_queen_check_diagonal():
    """Queen โจมตีทแยง"""
    board = """\
Q...
....
..K.
...."""
    assert run(board) == "Success"

def test_queen_blocked():
    """Queen ถูก Pawn บังทแยง → ไม่ check"""
    board = """\
Q...
.P..
..K.
...."""
    assert run(board) == "Fail"

# =============================================================================
#  6. First Piece Blocking  (ตัวแรกในเส้นทางจะบัง)
# =============================================================================
def test_rook_blocked_by_another_enemy():
    """Rook ถูก Bishop บังทาง → ไม่ถึง King"""
    board = """\
....
R.BK
....
...."""
    assert run(board) == "Fail"

def test_queen_blocked_by_pawn_vertical():
    """Queen ถูก Pawn บังแนวตั้ง"""
    board = """\
.Q..
....
.P..
.K.."""
    assert run(board) == "Fail"

# =============================================================================
#  7. Multiple Enemies — อย่างน้อยตัวหนึ่ง check ก็ Success
# =============================================================================
def test_multiple_enemies_one_checks():
    """หลายตัวศัตรู ตัวนึง check ได้"""
    board = """\
....
.K..
..P.
R..."""
    # P checks K (diagonal) → Success
    assert run(board) == "Success"

def test_multiple_enemies_none_checks():
    """หลายตัวศัตรู แต่ไม่มีใคร check ได้"""
    board = """\
....
.K..
.P..
..R."""
    # P ตรงข้างล่าง (ไม่ check), R ทแยง (ไม่ check)
    assert run(board) == "Fail"

# =============================================================================
#  8. Board Size ต่าง ๆ  (ต้องเป็นสี่เหลี่ยมจัตุรัส)
# =============================================================================
def test_1x1_king_only():
    """บอร์ด 1x1 มีแค่ King → Fail"""
    board = "K"
    assert run(board) == "Fail"

def test_2x2_board():
    """บอร์ด 2x2 — Rook ตรงแถวเดียวกับ King"""
    board = """\
R.
.K"""
    assert run(board) == "Fail"

def test_3x3_board():
    """บอร์ด 3x3"""
    board = """\
..B
...
K.."""
    assert run(board) == "Success"

def test_5x5_board():
    """บอร์ด 5x5 — Rook ตรง column เดียวกับ King → check"""
    board = """\
.....
.K...
.....
.....
.R..."""
    assert run(board) == "Success"  # R อยู่ column เดียวกับ K

def test_8x8_standard():
    """บอร์ด 8x8 มาตรฐาน — King ปลอดภัย"""
    board = """\
........
........
........
...K....
........
........
........
.......R"""
    assert run(board) == "Fail"  # R ไม่ตรงแถว/คอลัมน์เดียวกับ K

def test_8x8_rook_check():
    """บอร์ด 8x8 — Rook check King same row"""
    board = """\
........
........
........
R..K....
........
........
........
........"""
    assert run(board) == "Success"

# =============================================================================
#  9. Edge & Corner Cases  (King/ตัวหมากอยู่ขอบ/มุม)
# =============================================================================
def test_king_corner_check():
    """King อยู่มุม ถูก Rook check"""
    board = """\
...R
....
....
K..."""
    assert run(board) == "Fail"  # ไม่ตรงแถว ไม่ตรง col

def test_king_corner_rook_same_col():
    """King อยู่มุมล่างซ้าย Rook อยู่มุมบนซ้าย → check"""
    board = """\
R...
....
....
K..."""
    assert run(board) == "Success"

def test_king_edge():
    """King อยู่ขอบ ถูก Queen check ทแยง"""
    board = """\
...Q
....
.K..
...."""
    assert run(board) == "Success"

# =============================================================================
#  10. Error Handling / Invalid Input
# =============================================================================
def test_no_king():
    """ไม่มี King → Error (prints nothing or error msg)"""
    board = """\
R...
....
..P.
...."""
    result = run(board)
    assert result != "Success" and result != "Fail", "No King should return error"

def test_two_kings():
    """มี King 2 ตัว → Error"""
    board = """\
K...
....
..K.
...."""
    result = run(board)
    assert result != "Success" and result != "Fail", "Two Kings should return error"

def test_not_square_board():
    """บอร์ดไม่เป็นสี่เหลี่ยมจัตุรัส → Error"""
    board = """\
R....
.K..
..P.
...."""
    result = run(board)
    assert result != "Success" and result != "Fail", "Non-square board should return error"

def test_board_too_big():
    """บอร์ดใหญ่เกิน 8x8 → Error"""
    board = """\
.........
.........
.........
.........
.........
.........
.........
.........
....K...."""
    result = run(board)
    assert result != "Success" and result != "Fail", "Board > 8 rows should return error"

def test_empty_board():
    """บอร์ดว่างเปล่า → Error (ไม่มี King)"""
    board = ""
    result = run(board)
    assert result != "Success" and result != "Fail", "Empty board should return error"

def test_unknown_characters_treated_as_empty():
    """ตัวอักษรที่ไม่รู้จัก ถือเป็นช่องว่าง"""
    board = """\
RxZz
xKxx
xxPx
xxxx"""
    # x,Z,z → '.' ดังนั้น Rook row0 col0 เดินลง col0 → ถูกบังไหม?
    # R(0,0) เดินขวา: (0,1)='.', (0,2)='.', (0,3)='.' → ไม่ถึง K
    # R(0,0) เดินลง: (1,0)='.', (2,0)='.', (3,0)='.' → ไม่ถึง K
    # P(2,2) ทแยงบน: (1,1)=K → Success!
    assert run(board) == "Success"

# =============================================================================
#  11. Pawn Direction Edge Cases
# =============================================================================
def test_pawn_top_row():
    """Pawn อยู่แถวบนสุด → ไม่มีช่องให้โจมตี"""
    board = """\
.P..
..K.
....
...."""
    assert run(board) == "Fail"  # P โจมตีขึ้นบน ซึ่งหลุดบอร์ด

def test_pawn_adjacent_same_row():
    """Pawn อยู่แถวเดียวกับ King → ไม่ check"""
    board = """\
....
.PKK
....
...."""
    # ต้อง error เพราะมี 2 King — ลองเปลี่ยน
    # ใช้ P ข้างๆ K แทน
    board2 = """\
....
.PK.
....
...."""
    assert run(board2) == "Fail"

# =============================================================================
#  12. Bishop Long-range Diagonal
# =============================================================================
def test_bishop_long_diagonal():
    """Bishop โจมตี King จากมุมไกล"""
    board = """\
........
........
........
........
........
........
.......K
B......."""
    assert run(board) == "Fail"  # ไม่อยู่ diagonal เดียวกัน

def test_bishop_full_diagonal_8x8():
    """Bishop check King ข้ามทั้งบอร์ด"""
    board = """\
B.......
........
........
........
........
........
........
.......K"""
    assert run(board) == "Success"

# =============================================================================
#  13. Queen Combined Movement
# =============================================================================
def test_queen_vertical_check():
    """Queen check แนวตั้ง"""
    board = """\
..Q.
....
....
..K."""
    assert run(board) == "Success"

def test_queen_all_directions_fail():
    """Queen ถูกบังทุกทิศ → Fail"""
    board = """\
.....
.PBP.
.BQB.
.PBP.
..K.."""
    # Q ถูก B,P ล้อมรอบ → ไม่ถึง K
    assert run(board) == "Fail"

# =============================================================================
#  14. ตัวหมากบัง King (Piece blocks another piece)
# =============================================================================
def test_enemy_blocks_enemy():
    """ศัตรูบัง ศัตรูตัวอื่น"""
    board = """\
R..B
....
....
...K"""
    # R เดินขวา ถูก B บัง → R ไม่ถึง K
    # B(0,3) เดินทแยงลง-ซ้าย: (1,2),(2,1),(3,0) → ไม่ถึง K(3,3)
    # B(0,3) เดินลง: Bishop ไม่เดินตรง
    # R เดินลง col 0 → ไม่ถึง K
    assert run(board) == "Fail"

# =============================================================================
#  Run all tests
# =============================================================================
if __name__ == "__main__":
    tests = [
        # Subject examples
        ("Example1 (Rook checks King)", test_example1),
        ("Example2 (No enemy)", test_example2),
        # Pawn
        ("Pawn check left diagonal", test_pawn_check_left_diagonal),
        ("Pawn check right diagonal", test_pawn_check_right_diagonal),
        ("Pawn no check same column", test_pawn_no_check_same_column),
        ("Pawn no check behind", test_pawn_no_check_behind),
        ("Pawn no check too far", test_pawn_no_check_too_far),
        # Rook
        ("Rook check horizontal", test_rook_check_horizontal),
        ("Rook check vertical", test_rook_check_vertical),
        ("Rook blocked by piece", test_rook_blocked_by_piece),
        ("Rook no check diagonal", test_rook_no_check_diagonal),
        # Bishop
        ("Bishop check diagonal", test_bishop_check_diagonal),
        ("Bishop blocked", test_bishop_blocked),
        ("Bishop no check straight", test_bishop_no_check_straight),
        # Queen
        ("Queen check horizontal", test_queen_check_horizontal),
        ("Queen check diagonal", test_queen_check_diagonal),
        ("Queen blocked", test_queen_blocked),
        # Blocking
        ("Rook blocked by another enemy", test_rook_blocked_by_another_enemy),
        ("Queen blocked by pawn vertical", test_queen_blocked_by_pawn_vertical),
        # Multiple enemies
        ("Multiple enemies one checks", test_multiple_enemies_one_checks),
        ("Multiple enemies none checks", test_multiple_enemies_none_checks),
        # Board sizes
        ("1x1 King only", test_1x1_king_only),
        ("2x2 board", test_2x2_board),
        ("3x3 board", test_3x3_board),
        ("5x5 board", test_5x5_board),
        ("8x8 standard (safe)", test_8x8_standard),
        ("8x8 Rook check", test_8x8_rook_check),
        # Edge/corner
        ("King corner check", test_king_corner_check),
        ("King corner Rook same col", test_king_corner_rook_same_col),
        ("King edge Queen diagonal", test_king_edge),
        # Error handling
        ("No King", test_no_king),
        ("Two Kings", test_two_kings),
        ("Not square board", test_not_square_board),
        ("Board too big", test_board_too_big),
        ("Empty board", test_empty_board),
        ("Unknown chars as empty", test_unknown_characters_treated_as_empty),
        # Pawn edge cases
        ("Pawn top row", test_pawn_top_row),
        ("Pawn same row", test_pawn_adjacent_same_row),
        # Bishop long range
        ("Bishop long diagonal miss", test_bishop_long_diagonal),
        ("Bishop full diagonal 8x8", test_bishop_full_diagonal_8x8),
        # Queen combined
        ("Queen vertical check", test_queen_vertical_check),
        ("Queen all blocked", test_queen_all_directions_fail),
        # Piece blocks piece
        ("Enemy blocks enemy", test_enemy_blocks_enemy),
    ]

    passed = 0
    failed = 0
    errors = []

    for name, func in tests:
        try:
            func()
            print(f"  [PASS] {name}")
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {name} - {e}")
            failed += 1
            errors.append(name)
        except Exception as e:
            print(f"  [FAIL] {name} - {type(e).__name__}: {e}")
            failed += 1
            errors.append(name)

    print(f"\n{'='*50}")
    print(f"  Results: {passed} passed, {failed} failed, {passed + failed} total")
    if errors:
        print(f"  Failed tests:")
        for e in errors:
            print(f"    - {e}")
    print(f"{'='*50}")
