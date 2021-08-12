from collections import defaultdict

import torch
import numpy as np
from scipy.spatial.distance import cdist


def spmmsp(
    sp1: torch.sparse.Tensor,
    sp2: torch.sparse.Tensor
) -> torch.sparse.Tensor:
    from torch_sparse import spspmm
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


def label_to_tensor(label, num_classes, device=torch.device('cpu')):
    max_length = max([len(_l) for _l in label])
    index = [_l + _l[-1:] * (max_length - len(_l)) for _l in label]
    index = torch.LongTensor(index)
    return torch.zeros(
        (len(label), num_classes), device=device
    ).scatter_(1, index, 1)


def tensor_to_label(tensor, threshold=0.5):
    label_list, label_dict = [], defaultdict(list)
    labels = (tensor > threshold).nonzero(as_tuple=False)
    for label in labels:
        label_dict[label[0].item()].append(label[1].item())
    for _, label_value in label_dict.items():
        label_list.append(label_value)
    return label_list 


def get_dist_matrix(
    a: np.ndarray, b: np.ndarray
):
    return cdist(a, b)
    # aSumSquare = np.sum(np.square(a), axis=1)
    # bSumSquare = np.sum(np.square(b), axis=1)
    # mul = np.dot(a, b.T)
    # dists = np.sqrt(aSumSquare[:, np.newaxis] + bSumSquare - 2 * mul)
    # return dists