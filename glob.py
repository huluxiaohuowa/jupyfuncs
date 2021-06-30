import os
import inspect
import fnmatch

__all__ = [
    'recursive_glob',
]


def recursive_glob(treeroot, pattern):
    results = []
    for base, dirs, files in os.walk(treeroot):
        goodfiles = fnmatch.filter(files, pattern)
        results.extend(os.path.join(base, f) for f in goodfiles)
    return results


def makedirs(path: str, isfile: bool = False) -> None:
    """Creates a directory given a path to either a directory or file.
    If a directory is provided, creates that directory. If a file is provided (i.e. :code:`isfile == True`),
    creates the parent directory for that file.


    Args:
        path (str): Path to a directory or file. 
        isfile (bool, optional): Whether the provided path is a directory or file.Defaults to False.
    """    
    if isfile:
        path = os.path.dirname(path)
    if path != '':
        os.makedirs(path, exist_ok=True)


def get_current_dir():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
