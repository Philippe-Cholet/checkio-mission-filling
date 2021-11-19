"""
TESTS is a dict with all you tests.
Keys for this will be categories' names.
Each test is dict with
    "input" -- input data for user function
    "answer" -- your right answer
    "explanation" -- not necessary key, it's using for additional info in animation.
"""

SPECS = '''\
3x3:a2c2a1a
5x5:b21a33b4c44223b5d
8x6:1a1a14b3a23c4c1b514a13a1b5f8b121c
5x5:44a1b4b212b3c3b2a2a
8x6:2b3c24a42c8a2b38g28812c36c4e
9x7:2a477a7664b777b6b1f5c5b44e4b37a7a2b6c2a4a4a2
11x8:7773d7b77b8a442c88a8a2a7c775c56c7a78a4266f4k6a4a23a35b5b2a
10x10:a3a466b2a33c6a333b7a77e3a3a24221c8a4d2b88c2242d4b5f533a3c666a4a2a4e44
9x13:35c364d4f5a4c5a4d6d4a7a3a5b67b4b5c6a87c772887c77c332a3a6a2g3a4c5c7b435a5c7a
13x9:6c3d4c36a52d52a4a8d5b7b2c5b62b3a3b6c7c8d4c66e33e35a5552c993a4d3h4a21
10x15:b34d2c6e345a4b4a2b45g2d366a44d8a8c36b6c2a2d8g243a2a444c6a4a2c8326b4c3c7b885b58c4b6h3a38d
17x13:a666b5d92a3c666b32d3a4b134429f263553d4444g5c1i8f2333a7a2b64a54b42b7c4a6b4a3b65a7i3366a5b52c4a798b8a9b9b4a2a7a2a88a99f5a7c32a3c24a5a23b24d2f7a2
16x18:a2g8d2b4c5b6665a3c4a2545c7a9a9b8e555b799a7a7c89a9b9d77b6c99a2a69c7a5566a5b5b88b3b5a66a63a33c9a6c2e74b4c6b2a442i9a3f5d7b4b9a94644a4f4b2e69a9a92c8b34a4d33a85c9d9b28e9b77a2a7d75c95b3e4a2
20x20:b5a3a29a2b5a46b4a55d9c555b6b44c69999d7338a3a3c8a3c5d8c8b98c84a44b46d6c3a66g7b32d24c55b5a7a5c2a9a557d7a2888b89c55b254466c6b7c7k24d4b9a223b4a1b3349a9f88b4f6a559a74a8a8a2a663d5d26a99c9a66c2a3a3c9998e788885f5a88b377a8c3a2a85a88e47c7e5a4b87b7b37a533d9e7a5b5c4a8a89a4e
20x25:4d2b2a3b4b74c25h3a7b5a54c4a5a441c3a3b2d626b4b337g6a4a5g4a24e43b7a7c7b3777a3b66a8a3e27a77a2c6c5542c32b13a3a2d5b32a44e4b77a59b9b6b6613447a7a3b3a4a445b3c176c3a2b7a44d4d55e774b228d87d5a2d3c85b4c5b5a62b66b6b4a73c12266b34c1225h6b76f8e44d4c6655a338864a227b6d55a4b4c6b66a2b4999a9a3e9e2a999a2d635b94a7d3a5a5a66a36a668a8a7a337b5d2f84h8b
25x20:a2e3a2f429b32d355b5b46a6b3f9b66a4c42d44c5a5444a6677a53a7b73a26c6a2c2c7779a9d55b6b4c7b7b7a9b7775c5a5a5a5e48c7a7a6a69b99c2a88a3a2e35a55b4a2a4b8a86a8b443a2c3a3a7a7g6f1a447b72b7c6866a555552a44b5b57776b288d7a66b337f8b6b884b64d65c6b446666994c333e55a68i4a6b2a7a73a3a3a881888a6b68884a7a88b9a9c448a88d8b778c9a4a22443a3c3a355a26a229b4d6e4e3d99a3555a34d3b2b5a52a
'''.splitlines()


def spec2grid(spec):
    dim, line = spec.split(':')
    # Decompress the line:  a --> 0 ; b --> 00 ; c --> 000 ; ...
    for i in range(26):
        line = line.replace(chr(ord('a') + i), '0' * (i + 1))
    ncols, nrows = map(int, dim.split('x'))
    rows = (line[i * ncols: (i + 1) * ncols] for i in range(nrows))
    return [list(map(int, row)) for row in rows]


TESTS = {'Basics': [], 'Extra': []}

for n, grid in enumerate(map(spec2grid, SPECS)):
    category = ('Basics', 'Extra')[n > 2]
    TESTS[category].append({'input': grid, 'answer': grid})


if __name__ == '__main__':
    # ----- for initial code ----- #
    categories = ['Basics']  # + ['Extra']
    GRIDS = tuple(d['input'] for cat in categories for d in TESTS[cat])
    print('GRIDS =', GRIDS)

    # ----- for task descriptions ----- #
    url = 'https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/%s.html'
    url %= 'filling'
    for index, spec in enumerate(SPECS, 1):
        grid = spec2grid(spec)
        nrows, ncols = len(grid), len(grid[0])
        print(
            f'\t<a href="{url}#{spec}" title="{nrows} rows, {ncols} columns"'
            f' target="_blank">{index}</a>'
        )
