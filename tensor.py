import torch
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
