import os
import typing as t
import inspect
import fnmatch
import linecache
import time
import gc
import psutil
from os import path as osp
import pathlib
import sys
import importlib
import subprocess

import multiprocess as mp

__all__ = [
    'recursive_glob',
    'makedirs',
    'get_current_dir',
]


def recursive_glob(treeroot, pattern):
    """Recursively searches for files matching a specified pattern starting from the given directory.
    
    Args:
        treeroot (str): The root directory to start the search from.
        pattern (str): The pattern to match the files against.
    
    Returns:
        list: A list of file paths that match the specified pattern.
    """
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
    """Return the current directory path."""
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def get_num_lines(file):
    """Get the number of lines in a file.
    
    Args:
        file (str): The path to the file.
    
    Returns:
        int: The number of lines in the file.
    """
    num_lines = subprocess.check_output(
        ['wc', '-l', file]
    ).split()[0]
    return int(num_lines)


def str_from_line(file, line, split=False):
    """Retrieve a specific line from a file and process it.
    
    Args:
        file (str): The path to the file.
        line (int): The line number to retrieve (starting from 0).
        split (bool, optional): If True, split the line by space or tab and return the first element. Defaults to False.
    
    Returns:
        str: The content of the specified line from the file.
    """
    smi = subprocess.check_output(
        # ['sed','-n', f'{str(i+1)}p', file]
        ["sed", f"{str(line + 1)}q;d", file]
    )
    if isinstance(smi, bytes):
        smi = smi.decode().strip()
    if split:
        if ' ' or '\t' in smi:
            smi = smi.split()[0]
    return smi


def splitted_strs_from_line(
    file: str,
    idx: int
) -> t.List:
    """Return a list of strings obtained by splitting the line at the specified index from the given file.
    
        Args:
            file (str): The file path.
            idx (int): The index of the line to split.
    
        Returns:
            List: A list of strings obtained by splitting the line at the specified index.
    """
    return str_from_line(file, idx).split()


def chunkify_file(
    fname,
    size=1024 * 1024 * 1000,
    skiplines=-1
):
    """
    function to divide a large text file into chunks each having size ~= size so that the chunks are line aligned

    Params : 
        fname : path to the file to be chunked
        size : size of each chink is ~> this
        skiplines : number of lines in the begining to skip, -1 means don't skip any lines
    Returns : 
        start and end position of chunks in Bytes
    """
    chunks = []
    fileEnd = os.path.getsize(fname)
    with open(fname, "rb") as f:
        if(skiplines > 0):
            for i in range(skiplines):
                f.readline()

        chunkEnd = f.tell()
        count = 0
        while True:
            chunkStart = chunkEnd
            f.seek(f.tell() + size, os.SEEK_SET)
            f.readline()  # make this chunk line aligned
            chunkEnd = f.tell()
            chunks.append((chunkStart, chunkEnd - chunkStart, fname))
            count += 1

            if chunkEnd > fileEnd:
                break
    return chunks


def parallel_apply_line_by_line_chunk(chunk_data):
    """
    function to apply a function to each line in a chunk

    Params :
        chunk_data : the data for this chunk 
    Returns :
        list of the non-None results for this chunk
    """
    chunk_start, chunk_size, file_path, func_apply = chunk_data[:4]
    func_args = chunk_data[4:]

    # t1 = time.time()
    chunk_res = []
    with open(file_path, "rb") as f:
        f.seek(chunk_start)
        cont = f.read(chunk_size).decode(encoding='utf-8')
        lines = cont.splitlines()

        for _, line in enumerate(lines):
            ret = func_apply(line, *func_args)
            if(ret != None):
                chunk_res.append(ret)
    return chunk_res


def parallel_apply_line_by_line(
    input_file_path,
    chunk_size_factor,
    num_procs,
    skiplines,
    func_apply,
    func_args,
    fout=None
):
    """
    function to apply a supplied function line by line in parallel

    Params :
        input_file_path : path to input file
        chunk_size_factor : size of 1 chunk in MB
        num_procs : number of parallel processes to spawn, max used is num of available cores - 1
        skiplines : number of top lines to skip while processing
        func_apply : a function which expects a line and outputs None for lines we don't want processed
        func_args : arguments to function func_apply
        fout : do we want to output the processed lines to a file
    Returns :
        list of the non-None results obtained be processing each line
    """
    num_parallel = min(num_procs, psutil.cpu_count()) - 1

    jobs = chunkify_file(input_file_path, 1024 * 1024 * chunk_size_factor, skiplines)

    jobs = [list(x) + [func_apply] + func_args for x in jobs]

    print("Starting the parallel pool for {} jobs ".format(len(jobs)))

    lines_counter = 0

    pool = mp.Pool(num_parallel, maxtasksperchild=1000)  # maxtaskperchild - if not supplied some weird happend and memory blows as the processes keep on lingering

    outputs = []
    for i in range(0, len(jobs), num_parallel):
        print("Chunk start = ", i)
        t1 = time.time()
        chunk_outputs = pool.map(
            parallel_apply_line_by_line_chunk,
            jobs[i: i + num_parallel]
        )

        for i, subl in enumerate(chunk_outputs):
            for x in subl:
                if(fout != None):
                    print(x, file=fout)
                else:
                    outputs.append(x)
                lines_counter += 1
        del(chunk_outputs)
        gc.collect()
        print("All Done in time ", time.time() - t1)

    print("Total lines we have = {}".format(lines_counter))

    pool.close()
    pool.terminate()
    return outputs


def get_func_from_dir(score_dir: str) -> t.Tuple[t.Callable, str]:
    """Get function and mode from directory.
    
    Args:
        score_dir (str): The directory path containing the function file.
        
    Returns:
        Tuple[Callable, str]: A tuple containing the main function and the mode.
    """
    if score_dir.endswith('.py'):
        func_dir = pathlib.Path(score_dir).parent.resolve()
        file_name = pathlib.Path(score_dir).stem
    else:
        func_dir = osp.abspath(score_dir)
        file_name = "main"

    sys.path.append(func_dir)
    module = importlib.import_module(file_name) 
    try:
        mode = module.MODE
    except Exception as _:
        mode = 'batch'
    return module.main, mode 