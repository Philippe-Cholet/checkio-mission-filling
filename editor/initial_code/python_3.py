from typing import List#, Tuple

def filling(grid: List[List[int]]) -> List[List[int]]: # Tuple[Tuple[int]]
    # your code here
    return grid


if __name__ == '__main__':
    def checker(function, input_grid):
        input_copy = [row[:] for row in input_grid]
        result = function(input_copy)
        # 1) Check all types.
        if not (isinstance(result, (tuple, list)) and \
                all(isinstance(row, (tuple, list)) for row in result) and \
                all(isinstance(n, int) for row in result for n in row)):
            print("The result must be a list/tuple of lists/tuples of ints.")
            return False
        # 2) Check all sizes.
        nb_rows, nb_cols = len(input_grid), len(input_grid[0])
        if not (len(result) == nb_rows and \
                all(len(row) == nb_cols for row in result)):
            print("The result must have the same size as input grid.")
            return False
        # 3) Check if there is any forbidden change.
        # And if the contents of the result grid is possible.
        for i, (row, res_row) in enumerate(zip(input_grid, result)):
            for j, (n, res_n) in enumerate(zip(row, res_row)):
                if n and res_n != n:
                    print(f"You should not have changed {n} "
                          f"to {res_n} in the grid at {(i, j)}.")
                    return False
                if not (0 < res_n <= 9):
                    print(f"{res_n} is impossible at {(i, j)}.")
                    return False
        # 4) Is it filled properly? Thanks to DFS on all connected components.
        visited = {(i, j): False for i in range(nb_rows)
                                 for j in range(nb_cols)}
        while True:
            try:
                start = i, j = next(coord for coord, visit in visited.items()
                                          if not visit)
            except StopIteration:
                break
            stack, nb, count = [start], result[i][j], 0
            while stack:
                i, j = stack.pop()
                visited[i, j] = True
                count += 1
                for x, y in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if 0 <= x < nb_rows and 0 <= y < nb_cols and \
                       not visited[x, y] and result[x][y] == nb:
                        stack.append((x, y))
            if count != nb:
                print(f"Zone at {start} should have {nb} elements, not {count}.")
                return False
        return True

    GRIDS = (('5x5', [[1, 4, 0, 1, 0],
                      [0, 0, 1, 0, 0],
                      [0, 1, 0, 1, 4],
                      [0, 5, 0, 4, 2],
                      [0, 0, 0, 1, 0]]),

             ('6x8', [[1, 0, 1, 0, 1, 4, 0, 0],
                      [3, 0, 2, 3, 0, 0, 0, 4],
                      [0, 0, 0, 1, 0, 0, 5, 1],
                      [4, 0, 1, 3, 0, 1, 0, 0],
                      [5, 0, 0, 0, 0, 0, 0, 8],
                      [0, 0, 1, 2, 1, 0, 0, 0]]))

    for dim, grid in GRIDS:
        assert checker(filling, grid), f'You failed with the grid {dim}.'

    print('The local tests are done. Click on "Check" for more real tests.')
