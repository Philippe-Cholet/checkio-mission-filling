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

"""
@kurosawa4434
The checker sends (message, list of the problematic cell positions)
to you for javascript visualization.

You could simply display the problematic cells in red, and show the error
message if any. If there is an error message but no problematic cell, then the
grid is fully wrong (types or sizes) and should not be displayed at all.
"""


def checker(input_grid, result):
    try:
        # 1) Check types.
        assert isinstance(result, (tuple, list)) and all(
            isinstance(row, (tuple, list))
            and all(isinstance(n, int) and 0 <= n <= 9 for n in row)
            for row in result
        ), ('The result must be a list of lists of ints between 0 and 9.', [])
        # 2) Check sizes.
        nrows, ncols = len(input_grid), len(input_grid[0])
        assert (
            len(result) == nrows and all(len(row) == ncols for row in result)
        ), ('The result must have the same sizes as the input grid.', [])
        # 3) Check if there is any forbidden change from the input grid.
        changes = [(i, j) for i, row in enumerate(input_grid)
                   for j, n in enumerate(row) if n != 0 and result[i][j] != n]
        assert not changes, (
            'You must not change non-empty cells in the given grid.', changes
        )
        # 4) Check if there is any empty cell in the result grid.
        empties = [(i, j) for i, row in enumerate(result)
                   for j, n in enumerate(row) if n == 0]
        assert not empties, (
            'There are %d empty cells.' % len(empties), empties
        )
        # 5) Check if the grid is filled the right way.
        unvisited = {(i, j) for i in range(nrows) for j in range(ncols)}
        while unvisited:
            start = i, j = min(unvisited)
            stack, cells, expected = [start], [], result[i][j]
            while stack:
                pos = i, j = stack.pop()
                if pos not in unvisited:
                    continue
                unvisited.remove(pos)
                cells.append(pos)
                for neighbor in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                    x, y = neighbor
                    if 0 <= x < nrows and 0 <= y < ncols:
                        if neighbor in unvisited and result[x][y] == expected:
                            stack.append(neighbor)
            assert len(cells) == expected, (
                'Zone at %s should have %d elements, not %d.'
                % (start, expected, len(cells)), sorted(cells)
            )
    except AssertionError as error:
        return False, error.args[0]
    return True, ('', [])


api.add_listener(
    ON_CONNECT,
    CheckiOReferee(
        tests=TESTS,
        checker=checker,
        function_name={
            'python': 'filling',
            # 'js': 'filling',
        },
    ).on_ready,
)
