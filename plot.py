from os import path as osp

import seaborn as sn
import sklearn
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

from .glob import get_num_lines, str_from_line

cm = matplotlib.cm.get_cmap('Paired')
colors = cm.colors

def get_metrics_curves(
    base_dir,
    ckpts,
    num_points,
    title="Metric Curve",
    metric='accuracy',
    log_file='metrics.log',
    label: str = 'training_size',
    save_dir: str = './metric.png',
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
        data_idx = 0
        for line_id in range(get_num_lines(log)):
            line = str_from_line(log, line_id).split()
            if len(line) == 3 and line[1].strip() == metric:
                data_idx += 1
                if label == 'num_episodes':
                    x = data_idx
                elif label == 'training_size':
                    x = int(line[0].strip())
                data_dict[ckpt].append(
                    [
                        x,
                        float(line[2].strip())
                    ]
                )
            if line_id >= num_points - 1:
                break
    plt.figure(figsize=(10, 6), dpi=300)
    # plt.style.use('ggplot')
    plt.title(title)
    for i, (ckpt, points) in enumerate(data_dict.items()):
        points_array = np.array(points).T
        plt.plot(points_array[0], points_array[1], label=ckpt, color=colors[i])
    plt.legend(loc='lower right')
    plt.xlabel(
        label
    )
    plt.ylabel(metric)
    plt.grid(True)
    plt.savefig(save_dir)
    plt.show()