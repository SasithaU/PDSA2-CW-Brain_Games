def solve_hanoi_recursive(n, source, destination, auxiliary, moves=None):
    if moves is None:
        moves = []
    if n == 1:
        moves.append((source, destination))
    else:
        solve_hanoi_recursive(n-1, source, auxiliary, destination, moves)
        moves.append((source, destination))
        solve_hanoi_recursive(n-1, auxiliary, destination, source, moves)
    return moves

def solve_hanoi_iterative(n, source, destination, auxiliary):
    moves = []
    pegs = {source: [], auxiliary: [], destination: []}

    # Initialize source peg with disks (largest to smallest)
    for i in range(n, 0, -1):
        pegs[source].append(i)

    # Determine actual destination and auxiliary based on number of disks
    if n % 2 == 0:
        auxiliary, destination = destination, auxiliary

    total_moves = 2 ** n - 1
    peg_names = [source, auxiliary, destination]

    for move in range(1, total_moves + 1):
        if move % 3 == 1:
            from_peg, to_peg = get_legal_move(pegs, source, destination)
        elif move % 3 == 2:
            from_peg, to_peg = get_legal_move(pegs, source, auxiliary)
        else:
            from_peg, to_peg = get_legal_move(pegs, auxiliary, destination)

        disk = pegs[from_peg].pop()
        pegs[to_peg].append(disk)
        moves.append((from_peg, to_peg))

    return moves

def get_legal_move(pegs, peg1, peg2):
    if not pegs[peg1]:
        return peg2, peg1
    elif not pegs[peg2]:
        return peg1, peg2
    elif pegs[peg1][-1] < pegs[peg2][-1]:
        return peg1, peg2
    else:
        return peg2, peg1
