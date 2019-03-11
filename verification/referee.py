"""
CheckiOReferee is a base referee for checking you code.
    arguments:
        tests -- the dict contains tests in the specific structure.
            You can find an example in tests.py.
        cover_code -- is a wrapper for the user function and additional operations before give data
            in the user function. You can use some predefined codes from checkio.referee.cover_codes
        checker -- is replacement for the default checking of an user function result. If given, then
            instead simple "==" will be using the checker function which return tuple with result
            (false or true) and some additional info (some message).
            You can use some predefined codes from checkio.referee.checkers
        add_allowed_modules -- additional module which will be allowed for your task.
        add_close_builtins -- some closed builtin words, as example, if you want, you can close "eval"
        remove_allowed_modules -- close standard library modules, as example "math"
checkio.referee.checkers
    checkers.float_comparison -- Checking function fabric for check result with float numbers.
        Syntax: checkers.float_comparison(digits) -- where "digits" is a quantity of significant
            digits after coma.
checkio.referee.cover_codes
    cover_codes.unwrap_args -- Your "input" from test can be given as a list. if you want unwrap this
        before user function calling, then using this function. For example: if your test's input
        is [2, 2] and you use this cover_code, then user function will be called as checkio(2, 2)
    cover_codes.unwrap_kwargs -- the same as unwrap_kwargs, but unwrap dict.
"""

from checkio import api
from checkio.signals import ON_CONNECT
from checkio.referees.io import CheckiOReferee
# from checkio.referees import cover_codes

from tests import TESTS


def checker(input_grid, result):
    # 1) Check all types.
    if not (isinstance(result, (tuple, list)) and
            all(isinstance(row, (tuple, list)) for row in result) and
            all(isinstance(n, int) for row in result for n in row)):
        return False, ("The result must be a list/tuple "
                       "of lists/tuples of ints.")
    # 2) Check all sizes.
    nb_rows, nb_cols = len(input_grid), len(input_grid[0])
    if not (len(result) == nb_rows and
            all(len(row) == nb_cols for row in result)):
        return False, "The result must have the same size as input grid."
    # 3) Check if there is any forbidden change.
    # And if the contents of the result grid is possible.
    for i, (row, res_row) in enumerate(zip(input_grid, result)):
        for j, (n, res_n) in enumerate(zip(row, res_row)):
            if n and res_n != n:
                return False, (f"You should not have changed {n} to {res_n} "
                               f"in the grid at {(i, j)}.")
            if not (0 < res_n <= 9):
                return False, f"{res_n} is impossible at {(i, j)}."
    # 4) Is it filled properly? Thanks to DFS on all connected components.
    visited = {(i, j): False for i in range(nb_rows) for j in range(nb_cols)}
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
                if (0 <= x < nb_rows and 0 <= y < nb_cols and
                        not visited[x, y] and result[x][y] == nb):
                    stack.append((x, y))
        if count != nb:
            return False, (f"Zone at {start} should have {nb} elements, "
                           f"not {count}.")
    return True, "Great!"


api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests=TESTS,
        checker=checker,
        function_name={
            "python": "filling",
            # "js": "filling"
        },
        ).on_ready
)
