import torch
import numpy as np
from torch_sparse import spspmm


__all__ = [
    "spmmsp",
]


def spmmsp(
    sp1: torch.sparse.Tensor,
    sp2: torch.sparse.Tensor
) -> torch.sparse.Tensor:
    assert sp1.size(-1) == sp2.size(0) and sp1.is_sparse and sp2.is_sparse
    m = sp1.size(0)
    k = sp2.size(0)
    n = sp2.size(-1)
    indices, values = spspmm(
        sp1.indices(), sp1.values(),
        sp2.indices(), sp2.values(),
        m, k, n
    )
    return torch.sparse_coo_tensor(
        indices,
        values,
        torch.Size([m, n])
    )


def label_to_onehot(ls, class_num):
    ls = ls.reshape(-1, 1)
    return torch.zeros(
        (len(ls), class_num), device=ls.device
    ).scatter_(1, ls, 1)


def onehot_to_label(tensor):
    if isinstance(tensor, torch.Tensor):
        return torch.argmax(tensor, dim=-1)
    elif isinstance(tensor, np.ndarray):
        return np.argmax(tensor, axis=-1)


def get_dist_matrix(
    a: np.array, b: np.array
):
    aSumSquare = np.sum(np.square(a), axis=1)
    bSumSquare = np.sum(np.square(b), axis=1)
    mul = np.dot(a, b.T)
    dists = np.sqrt(aSumSquare[:, np.newaxis] + bSumSquare - 2 * mul)
    return dists