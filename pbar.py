import sys
from IPython.core.display import HTML

__all__ = [
    'in_jupyter',
    'tqdm',
    'trange',
    'tnrange',
    'no_white',
]


def no_white():
    return HTML("""
    <style>
    .jp-OutputArea-prompt:empty {
    padding: 0;
    border: 0;
    }
    </style>
    """)



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