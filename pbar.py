import sys

__all__ = [
    'in_jupyter',
    'tqdm',
    'trange',
    'tnrange',
]


def in_jupyter():

    which = True if 'ipykernel_launcher.py' in sys.argv[0] else False
    return which


if in_jupyter():
    from tqdm.notebook import tqdm
    from tqdm.notebook import trange
    from tqdm.notebook import tnrange
else:
    from tqdm import tqdm
    from tqdm import trange
    from tqdm import tnrange