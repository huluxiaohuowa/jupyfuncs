def diff(listA, listB, mode="intersection"):
    #求交集的两种方式
    if mode == "intersection":
        ret = list(set(listA).intersection(set(listB)))
    elif mode == "union":
        ret = list(set(listA).union(set(listB)))
    elif mode == "diff":
        ret = list(set(listB).difference(set(listA)))
    
    return ret