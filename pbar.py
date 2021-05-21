import sys

__all__ = [
    'tqdm',
]

def in_jupyter():

    which = True if 'ipykernel_launcher.py' in sys.argv[0] else False
    return which


if in_jupyter():
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm