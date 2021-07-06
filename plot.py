from os import path as osp

import seaborn as sn
import sklearn
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .glob import get_num_lines, str_from_line


def accuracies_heat(y_true, y_pred, num_tasks):
    assert len(y_true) == len(y_pred)
    cm = sklearn.metrics.confusion_matrix(
        y_true, y_pred, normalize='true'
    )
    df_cm = pd.DataFrame(
        cm, range(num_tasks), range(num_tasks)
    )
    plt.figure(figsize=(10, 10))
    sn.set(font_scale=1.4) 
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}, fmt='.2f')


def get_metrics_curves(
    base_dir,
    ckpts,
    num_points,
    metric='accuracy',
    log_file='metrics.log'
):
    data_dict = {}
    for ckpt in ckpts:
        log = osp.join(
            base_dir,
            ckpt,
            log_file
        )
        if not osp.exists(log):
            print(f"WARNING: not log for {ckpt}")
            continue
        data_dict[ckpt] = []
        for line_id in range(get_num_lines(log)):
            line = str_from_line(log, line_id).split('\t')
            if len(line) == 3 and line[1].strip() == metric:
                data_dict[ckpt].append(
                    [int(line[0].strip()), float(line[2].strip())]
                )
            if line_id >= num_points - 1:
                break
    plt.figure(figsize=(10, 6), dpi=300)
    plt.style.use('ggplot')
    plt.title('Result Analysis')
    for ckpt, points in data_dict.items():
        points_array = np.array(points).T
        plt.plot(points_array[0], points_array[1], label=ckpt)
    plt.legend()
    plt.xlabel('Training size')
    plt.ylabel(metric)
    plt.grid(True)
    plt.show()