import os
import inspect
import fnmatch
import linecache

__all__ = [
    'recursive_glob',
    'makedirs',
    'get_current_dir',
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


def get_num_lines(
    input_file: str
) -> int:
    """Get num_of_lines of a text file
    Args:
        input_file (str): location of the file
    Returns:
        int: num_lines of the file
    Examples:
        >>> get_num_lines("./dataset.txt")
    """
    for num_lines, line in enumerate(open(input_file, 'r')):
        pass
    return num_lines + 1


def str_from_line(
    file: str,
    idx: int
) -> str:
    """
    Get string from a specific line
    Args:
        idx (int): index of line
        file (string): location of a file
    Returns:
    """
    return linecache.getline(file, idx + 1).strip()