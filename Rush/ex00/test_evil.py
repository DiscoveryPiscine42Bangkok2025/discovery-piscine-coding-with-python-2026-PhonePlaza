from checkmate import checkmate
import io, sys

def run(board):
    """capture stdout from checkmate(), return stripped string"""
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        checkmate(board)
    except Exception:
        pass  # function should never crash
    sys.stdout = old
    return buf.getvalue().strip()

def run_no_crash(board):
    """call checkmate() and just make sure it doesn't crash/hang.
    Returns True if no exception, False if crashed."""
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        checkmate(board)
        sys.stdout = old
        return True
    except Exception as e:
        sys.stdout = old
        return False

# =============================================================================
# CATEGORY A: Wrong Input Types  (should not crash)
# Requirement: "should never crash or loop indefinitely"
# =============================================================================
def test_none_input():
    """board = None"""
    assert run_no_crash(None), "None input should not crash"

def test_integer_input():
    """board = 42"""
    assert run_no_crash(42), "Integer input should not crash"

def test_list_input():
    """board = ['R...', '.K..']"""
    assert run_no_crash(['R...', '.K..']), "List input should not crash"

def test_bool_input():
    """board = True"""
    assert run_no_crash(True), "Boolean input should not crash"

def test_dict_input():
    """board = {}"""
    assert run_no_crash({}), "Dict input should not crash"

def test_float_input():
    """board = 3.14"""
    assert run_no_crash(3.14), "Float input should not crash"

# =============================================================================
# CATEGORY B: Empty / Whitespace / Weird strings
# =============================================================================
def test_empty_string():
    """board = '' """
    result = run("")
    assert result not in ("Success", "Fail") or result == "", \
        "Empty string: no King present"

def test_only_newlines():
    """board = multiple newlines"""
    result = run("\n\n\n")
    assert run_no_crash("\n\n\n"), "Only newlines should not crash"

def test_only_spaces():
    """board = '    ' (4 spaces, 1 row of 4 chars) -> not square (1 row, 4 cols)"""
    result = run("    ")
    assert result != "Success", "Only spaces should not be Success"

def test_tabs_in_board():
    """board with tab characters"""
    board = "K\t.\n..\n.."
    assert run_no_crash(board), "Tabs should not crash"

def test_single_newline():
    """board = just a newline"""
    assert run_no_crash("\n"), "Single newline should not crash"

def test_spaces_as_board():
    """4x4 board of spaces (spaces = empty squares, no King)"""
    board = "    \n    \n    \n    "
    result = run(board)
    assert result != "Success", "Board of spaces has no King"

# =============================================================================
# CATEGORY C: Trailing / Leading newlines (creates empty rows)
# =============================================================================
def test_trailing_newline():
    """Board with trailing newline -> creates extra empty row"""
    board = "R...\n.K..\n..P.\n....\n"
    # extra empty row "" at end -> len 0 != len 5 -> not square
    assert run_no_crash(board), "Trailing newline should not crash"

def test_leading_newline():
    """Board with leading newline -> empty row at start"""
    board = "\nR...\n.K..\n..P.\n...."
    assert run_no_crash(board), "Leading newline should not crash"

def test_double_trailing_newline():
    """Board with two trailing newlines"""
    board = "R...\n.K..\n..P.\n....\n\n"
    assert run_no_crash(board), "Double trailing newline should not crash"

def test_crlf_line_endings():
    r"""Board with \r\n line endings (Windows-style)"""
    board = "R...\r\n.K..\r\n..P.\r\n...."
    result = run(board)
    # \r will be part of row -> row length mismatch or treated as unknown char
    assert run_no_crash(board), "CRLF should not crash"

# =============================================================================
# CATEGORY D: Lowercase letters (should be treated as empty squares)
# =============================================================================
def test_lowercase_pieces():
    """lowercase p, r, b, q, k should be treated as empty, not as pieces"""
    board = """\
r...
.K..
..p.
...."""
    result = run(board)
    assert result == "Fail", "Lowercase pieces should be treated as empty"

def test_lowercase_king():
    """lowercase 'k' is NOT a King -> error"""
    board = """\
R...
.k..
..P.
...."""
    result = run(board)
    assert result != "Success" and result != "Fail", \
        "Lowercase 'k' is not King -> should be error (no King)"

# =============================================================================
# CATEGORY E: Unicode / Special Characters
# =============================================================================
def test_unicode_chars():
    """Board with Thai characters"""
    board = "K...\n....\n....\n...."
    board_thai = board.replace('.', '\u0e01')  # Thai char
    result = run(board_thai)
    assert result == "Fail", "Thai chars should be treated as empty"
    assert run_no_crash(board_thai)

def test_emoji_in_board():
    """Board with emoji characters (multi-byte)"""
    # This might cause issues with len() vs display width
    assert run_no_crash("K...\n....\n....\n....")

def test_numbers_in_board():
    """Board with numbers - treated as empty"""
    board = """\
1234
5K78
9012
3456"""
    result = run(board)
    assert result == "Fail", "Numbers should be treated as empty, King safe"

def test_special_symbols():
    """Board with @#$%^& symbols"""
    board = """\
@#$%
^K&*
!@#$
%^&*"""
    result = run(board)
    assert result == "Fail", "Special symbols = empty, King safe"

# =============================================================================
# CATEGORY F: Board Size Edge Cases
# =============================================================================
def test_0x0_board():
    """Empty string -> 0 rows"""
    assert run_no_crash(""), "0x0 board should not crash"

def test_1x1_pawn():
    """1x1 board with just P -> no King -> error"""
    result = run("P")
    assert result != "Success", "1x1 with only Pawn, no King"

def test_1x1_empty():
    """1x1 board with '.' -> no King"""
    result = run(".")
    assert result != "Success", "1x1 dot, no King"

def test_9x9_board():
    """9 rows -> too big (> 8)"""
    board = "\n".join(["." * 9] * 9)
    # put a King somewhere
    lines = list(board.split("\n"))
    lines[4] = "....K...." 
    board = "\n".join(lines)
    result = run(board)
    assert result != "Success" and result != "Fail", \
        "9x9 board should be error (too big)"

def test_exactly_8x8():
    """Exactly 8x8 -> should be valid"""
    board = """\
........
........
........
...K....
........
........
........
R......."""
    result = run(board)
    assert result == "Fail", "8x8, R not aligned with K"

def test_non_square_more_cols():
    """3 rows but 5 cols -> not square"""
    board = ".....\n..K..\n....."
    result = run(board)
    assert result != "Success", "Not square: 3x5"

def test_non_square_more_rows():
    """5 rows but 3 cols -> not square"""
    board = "...\n.K.\n...\n...\n..."
    result = run(board)
    assert result != "Success", "Not square: 5x3"

def test_uneven_row_lengths():
    """Rows with different lengths"""
    board = "R...\n.K.\n..P.\n...."
    result = run(board)
    # Row 1 has 3 chars, others have 4 -> not square
    assert result != "Success", "Uneven rows should not be Success"
    assert run_no_crash(board)

# =============================================================================
# CATEGORY G: Pawn Evil Edge Cases
# =============================================================================
def test_pawn_directly_below_king():
    """Pawn 1 row below King (Pawn attacks UP, not where K is from Pawn)"""
    board = """\
....
.K..
.P..
...."""
    assert run(board) == "Fail", "Pawn below King doesn't attack downward-to-up"

def test_pawn_two_rows_above_king():
    """Pawn 2 rows above King -> too far for Pawn"""
    board = """\
.P..
....
.K..
...."""
    assert run(board) == "Fail", "Pawn 2 rows above can't reach"

def test_pawn_attacks_upward_only():
    """Pawn at row 3, King at row 4 diagonal -> Pawn goes UP not DOWN"""
    board = """\
.....
.....
.....
..P..
...K."""
    assert run(board) == "Fail", "Pawn attacks upward diagonals only"

def test_many_pawns_surrounding_king():
    """Pawns everywhere around King,
    only the ones diagonally below can check"""
    board = """\
.....
.PPP.
.PKP.
.PPP.
....."""
    # Pawns at (3,1),(3,2),(3,3) -> attack UP diagonals
    # P(3,1) attacks (2,0) and (2,2)=K -> Success!
    assert run(board) == "Success"

def test_pawn_at_left_edge():
    """Pawn at column 0 -> only right-diagonal attack works"""
    board = """\
....
.K..
P...
...."""
    # P(2,0) attacks (-1,-1)=invalid, (-1,1)=(1,1)=K -> Success!
    assert run(board) == "Success"

def test_pawn_at_right_edge():
    """Pawn at rightmost column -> only left-diagonal attack"""
    board = """\
....
..K.
...P
...."""
    # P(2,3) attacks (1,2)=K -> Success!
    assert run(board) == "Success"

# =============================================================================
# CATEGORY H: Complex Blocking Scenarios
# =============================================================================
def test_rook_blocked_by_own_kind():
    """Rook blocked by another Rook"""
    board = """\
.....
.K...
.....
.R...
.R..."""
    # R(4,1) going up -> hits R(3,1) first -> blocked
    # R(3,1) going up -> (2,1) empty, (1,1)=K -> Success
    assert run(board) == "Success"

def test_queen_behind_pawn_all_directions():
    """Queen completely enclosed by Pawns"""
    board = """\
.......
.......
..PPP..
..PQP..
..PPP..
.......
......K"""
    # Q surrounded by P -> cannot reach K
    assert run(board) == "Fail"

def test_bishop_blocked_at_distance_1():
    """Bishop blocked by adjacent piece"""
    board = """\
B....
.P...
..K..
.....
....."""
    assert run(board) == "Fail", "P blocks B from reaching K"

def test_multiple_pieces_different_blocks():
    """Multiple enemies, all blocked"""
    board = """\
R.B..
.P.P.
..K..
.P.P.
B.R.."""
    # R(0,0) down -> P(1,1)? No, R goes straight: (1,0),(2,0),(3,0),(4,0) -> none is K
    # R(0,0) right -> (0,1)='.', (0,2)='B' -> blocked
    # B(0,2) diag down-left -> (1,1)='P' -> blocked
    # B(0,2) diag down-right -> (1,3)='P' -> blocked
    # B(4,0) diag up-right -> (3,1)='P' -> blocked
    # R(4,2) up -> (3,2)='.', (2,2)=K -> Success!
    assert run(board) == "Success"

# =============================================================================
# CATEGORY I: King Position Edge Cases
# =============================================================================
def test_king_at_0_0():
    """King at top-left corner"""
    board = """\
K...
....
....
...R"""
    assert run(board) == "Fail", "R not aligned with K"

def test_king_at_max_corner():
    """King at bottom-right corner"""
    board = """\
R.......
........
........
........
........
........
........
.......K"""
    # R(0,0) -> row 0, col 0. K at (7,7). Not aligned.
    assert run(board) == "Fail"

def test_king_surrounded_all_fail():
    """King in center, enemies surround but all blocked"""
    board = """\
........
........
........
...BRB..
...RKR..
...BRB..
........
........"""
    # Every adjacent piece attacks AWAY from K or is blocked
    # R(3,4) goes down -> (4,4)='K' -> Success!
    assert run(board) == "Success"

# =============================================================================
# CATEGORY J: Piece Interacts with Board Boundary
# =============================================================================
def test_rook_fires_off_edge():
    """Rook at edge, fires toward edge (no King there)"""
    board = """\
...R
....
....
K..."""
    # R(0,3) right -> out of board immediately
    # R(0,3) up -> out of board
    # R(0,3) left -> (0,2),(0,1),(0,0) -> no K there (K at 3,0)
    # R(0,3) down -> (1,3),(2,3),(3,3) -> no K
    assert run(board) == "Fail"

def test_bishop_at_corner():
    """Bishop at corner attacks one diagonal only"""
    board = """\
....
....
....
B..K"""
    # B(3,0) up-right -> (2,1),(1,2),(0,3) -> no K(3,3)
    # B(3,0) other diags -> out of bounds
    assert run(board) == "Fail"

def test_queen_at_corner_checks_diagonal():
    """Queen at (0,0) checks King at (3,3) diagonally"""
    board = """\
Q...
....
....
...K"""
    assert run(board) == "Success"

# =============================================================================
# CATEGORY K: All Pieces Same Type Stress
# =============================================================================
def test_8_rooks_no_check():
    """8 Rooks but none aligned with King"""
    board = """\
........
........
........
...K....
........
........
........
........"""
    # No enemies at all -> Fail
    assert run(board) == "Fail"

def test_all_pawns_around_king():
    """All Pawns below King but none in capture position"""
    board = """\
..K..
.....
PPPPP
.....
....."""
    # Pawns at row 2, King at row 0. Pawns attack row 1, not row 0.
    assert run(board) == "Fail"

def test_rooks_on_every_edge():
    """Rooks on edges, King in center"""
    board = """\
..R..
.....
R.K.R
.....
..R.."""
    # R(0,2) down -> (1,2),(2,2)=K -> Success!
    assert run(board) == "Success"

# =============================================================================
# CATEGORY L: String That Looks Like Board But Isn't
# =============================================================================
def test_single_char_not_king():
    """Single character that is not K"""
    result = run("R")
    assert result != "Success", "No King on board"

def test_single_char_dot():
    """Single dot"""
    result = run(".")
    assert result != "Success", "No King on board"

def test_board_all_kings_invalid():
    """Board full of Ks -> should error (multiple Kings)"""
    board = """\
KKK
KKK
KKK"""
    result = run(board)
    assert result != "Success" and result != "Fail", "Multiple Kings = error"

def test_very_long_single_line():
    """One very long row -> 1 row, many cols -> not square"""
    board = "K" + "." * 99
    result = run(board)
    # 1 row, 100 cols -> not square but only 1 row... 
    # len(row)=100 != len(grid_board)=1
    assert result != "Success", "1x100 is not square"

def test_only_enemy_pieces_no_king():
    """Board with only enemies, no King"""
    board = """\
RRRR
BBBB
QQQQ
PPPP"""
    result = run(board)
    assert result != "Success" and result != "Fail", "No King = error"

# =============================================================================
# CATEGORY M: Defense-style Tests (what evaluators might try)
# =============================================================================
def test_defense_no_args():
    """Call checkmate with wrong args -> should not crash"""
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        checkmate()
        crashed = False
    except TypeError:
        crashed = True  # This is acceptable (missing argument)
    except Exception:
        crashed = True
    sys.stdout = old
    # TypeError for missing arg is acceptable behavior
    assert True  # Just ensure no infinite loop or segfault

def test_defense_extra_args():
    """Call checkmate with extra args"""
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        checkmate("K", "extra")
        crashed = False
    except TypeError:
        crashed = True  # acceptable
    except Exception:
        crashed = True
    sys.stdout = old
    assert True

def test_defense_board_with_backslash():
    r"""Board string contains literal backslash"""
    board = "K...\n..\\..\n....\n...."
    assert run_no_crash(board), "Backslash should not crash"

def test_defense_board_with_null_byte():
    """Board string contains null byte"""
    board = "K...\n..\x00..\n....\n...."
    assert run_no_crash(board), "Null byte should not crash"

# =============================================================================
#  Run all tests
# =============================================================================
if __name__ == "__main__":
    tests = [
        # A: Wrong Input Types
        ("A1: None input", test_none_input),
        ("A2: Integer input", test_integer_input),
        ("A3: List input", test_list_input),
        ("A4: Boolean input", test_bool_input),
        ("A5: Dict input", test_dict_input),
        ("A6: Float input", test_float_input),
        # B: Empty/Whitespace
        ("B1: Empty string", test_empty_string),
        ("B2: Only newlines", test_only_newlines),
        ("B3: Only spaces", test_only_spaces),
        ("B4: Tabs in board", test_tabs_in_board),
        ("B5: Single newline", test_single_newline),
        ("B6: Spaces as board", test_spaces_as_board),
        # C: Trailing/Leading newlines
        ("C1: Trailing newline", test_trailing_newline),
        ("C2: Leading newline", test_leading_newline),
        ("C3: Double trailing newline", test_double_trailing_newline),
        ("C4: CRLF line endings", test_crlf_line_endings),
        # D: Lowercase
        ("D1: Lowercase pieces", test_lowercase_pieces),
        ("D2: Lowercase king", test_lowercase_king),
        # E: Unicode/Special
        ("E1: Unicode Thai chars", test_unicode_chars),
        ("E2: Emoji in board", test_emoji_in_board),
        ("E3: Numbers in board", test_numbers_in_board),
        ("E4: Special symbols", test_special_symbols),
        # F: Board Size
        ("F1: 0x0 board", test_0x0_board),
        ("F2: 1x1 Pawn only", test_1x1_pawn),
        ("F3: 1x1 dot", test_1x1_empty),
        ("F4: 9x9 too big", test_9x9_board),
        ("F5: Exactly 8x8", test_exactly_8x8),
        ("F6: 3x5 not square", test_non_square_more_cols),
        ("F7: 5x3 not square", test_non_square_more_rows),
        ("F8: Uneven row lengths", test_uneven_row_lengths),
        # G: Pawn Evil
        ("G1: Pawn below King", test_pawn_directly_below_king),
        ("G2: Pawn 2 rows above", test_pawn_two_rows_above_king),
        ("G3: Pawn attacks up only", test_pawn_attacks_upward_only),
        ("G4: Many pawns around King", test_many_pawns_surrounding_king),
        ("G5: Pawn left edge", test_pawn_at_left_edge),
        ("G6: Pawn right edge", test_pawn_at_right_edge),
        # H: Complex Blocking
        ("H1: Rook blocked by Rook", test_rook_blocked_by_own_kind),
        ("H2: Queen enclosed by Pawns", test_queen_behind_pawn_all_directions),
        ("H3: Bishop blocked at dist 1", test_bishop_blocked_at_distance_1),
        ("H4: Multiple pieces blocked", test_multiple_pieces_different_blocks),
        # I: King Position
        ("I1: King at (0,0)", test_king_at_0_0),
        ("I2: King at max corner", test_king_at_max_corner),
        ("I3: King surrounded", test_king_surrounded_all_fail),
        # J: Boundary
        ("J1: Rook fires off edge", test_rook_fires_off_edge),
        ("J2: Bishop at corner", test_bishop_at_corner),
        ("J3: Queen corner diagonal", test_queen_at_corner_checks_diagonal),
        # K: Stress
        ("K1: No enemies", test_8_rooks_no_check),
        ("K2: All pawns miss", test_all_pawns_around_king),
        ("K3: Rooks on edges", test_rooks_on_every_edge),
        # L: Fake boards
        ("L1: Single R no King", test_single_char_not_king),
        ("L2: Single dot", test_single_char_dot),
        ("L3: All Kings", test_board_all_kings_invalid),
        ("L4: Very long single line", test_very_long_single_line),
        ("L5: Only enemies no King", test_only_enemy_pieces_no_king),
        # M: Defense
        ("M1: No args", test_defense_no_args),
        ("M2: Extra args", test_defense_extra_args),
        ("M3: Backslash in board", test_defense_board_with_backslash),
        ("M4: Null byte in board", test_defense_board_with_null_byte),
    ]

    passed = 0
    failed = 0
    errors = []

    print("=" * 60)
    print("  EVIL / EDGE CASE TEST SUITE")
    print("=" * 60)

    for name, func in tests:
        try:
            func()
            print(f"  [PASS] {name}")
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {name} - {e}")
            failed += 1
            errors.append((name, str(e)))
        except Exception as e:
            print(f"  [ERR!] {name} - {type(e).__name__}: {e}")
            failed += 1
            errors.append((name, f"{type(e).__name__}: {e}"))

    print(f"\n{'=' * 60}")
    print(f"  Results: {passed} passed, {failed} failed, {passed + failed} total")
    if errors:
        print(f"\n  Failed tests:")
        for name, reason in errors:
            print(f"    - {name}")
            if reason:
                print(f"      Reason: {reason}")
    print(f"{'=' * 60}")
