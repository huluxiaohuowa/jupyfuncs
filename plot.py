import seaborn as sn
import sklearn
import matplotlib.pyplot as plt
import pandas as pd


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