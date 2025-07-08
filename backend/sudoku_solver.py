# sudoku_solver.py (Fixed version)

def cross(A, B):
    return [a + b for a in A for b in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)

unitlist = (
    [cross(rows, c) for c in cols] +
    [cross(r, cols) for r in rows] +
    [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
)

units = {s: [u for u in unitlist if s in u] for s in squares}
peers = {s: set(sum(units[s], [])) - {s} for s in squares}


def grid_values(grid_str):
    """Convert grid string to {square: char} dict (expects length 81)."""
    assert len(grid_str) == 81
    return dict(zip(squares, grid_str))


def parse_grid(grid_str):
    """Convert grid to dict of {square: digits}, or return False if contradiction."""
    values = {s: digits for s in squares}
    for s, d in grid_values(grid_str).items():
        if d in digits and not assign(values, s, d):
            return False
    return values


def assign(values, s, d):
    """Assign d to square s, removing all other values, and propagate."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2."""
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d, '')
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values


def search(values):
    """Use depth-first search and propagation to try all possibilities."""
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in squares):
        return values
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])


def some(seq):
    for e in seq:
        if e: return e
    return False


def solve_grid(grid):
    """Solve a 9x9 Sudoku grid. Empty cells can be represented as empty strings or any non-digit character."""
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError("Grid must be 9x9")

    # Convert grid to flat string, replacing empty/invalid cells with '.'
    flat = ''.join([
        cell if isinstance(cell, str) and len(cell) == 1 and cell in digits 
        else '.' 
        for row in grid 
        for cell in row
    ])

    if len(flat) != 81:
        raise ValueError(f"Flattened grid has {len(flat)} characters, expected 81.")

    result = search(parse_grid(flat))

    if not result:
        return None

    return [[result[r + c] for c in cols] for r in rows]


# Test the solver
if __name__ == "__main__":
    input_grid = [
        ["1", "", "7", "", "", "6", "4", "5", ""],
        ["", "2", "5", "3", "4", "", "", "", "8"],
        ["", "6", "", "", "", "1", "", "7", ""],
        ["", "5", "3", "", "", "", "", "2", "9"],
        ["6", "1", "", "", "", "9", "8", "", ""],
        ["", "", "", "6", "", "2", "", "", "7"],
        ["", "", "1", "", "9", "3", "2", "", ""],
        ["", "", "8", "", "", "", "", "", ""],
        ["", "4", "", "", "7", "8", "5", "9", "1"],
    ]

    result = solve_grid(input_grid)

    if result:
        print("Solved Grid:")
        for row in result:
            print(row)
    else:
        print("Unsolvable grid")