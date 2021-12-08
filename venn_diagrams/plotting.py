import pathlib
import matplotlib.pyplot as plt
from matplotlib_venn import (venn2, venn2_circles, venn2_unweighted, venn3, venn3_circles)

def get_ribo_seq_venn(dl_set: set, ribo_set: set, dl_name: str, ribo_name: str, 
                      save: bool = False, save_dir: pathlib.Path = None, 
                      circle_name_size: int = 20, circle_number_size: list = [16, 16, 16]):
    plt.figure(figsize=(4,4))
    out = venn2((dl_set, ribo_set), 
                (dl_name, ribo_name),
                set_colors=('silver', 'silver'), )
                # alpha = 0.8)
    venn2_circles((dl_set, ribo_set), 
                linestyle='-', 
                linewidth=1, 
                color='darkgrey')
    for text in out.set_labels:
        text.set_fontsize(circle_name_size)
    for i, text in enumerate(out.subset_labels):
        text.set_fontsize(circle_number_size[i])
    # plt.title('Representation Score: 1.0\np-value < 0.497\n # common lncRNAs = 1718',fontsize=18 )
    if save:
        plt.savefig(save_dir, dpi=200, bbox_inches='tight')


def intersection_dl_models_venn(cnn_misannots: set, lstm_misannots: set, transf_misannots: set, save: bool = False, save_dir: pathlib.Path = None):
    plt.figure(figsize=(4,4))
    out = venn3((cnn_misannots, lstm_misannots, transf_misannots),
                set_labels=('CNN', 'LSTM', 'Transformer'), 
                set_colors=('silver', 'silver','silver'), )
                # alpha = 0.8)
    venn3_circles([cnn_misannots, lstm_misannots, transf_misannots], 
                linestyle='-', 
                linewidth=1, 
                color='darkgrey')
    for text in out.set_labels:
        text.set_fontsize(16)
    for text in out.subset_labels:
        text.set_fontsize(14)
    if save:
        plt.savefig(save_dir, dpi=50, bbox_inches='tight')


def cncrnadb_venn(dl_set: set, cnc_set: set, dl_name: str, cnc_name: str = 'cncRNA\nDatabase', 
                  save: bool = False, save_dir: pathlib.Path = None, 
                  circle_name_size: int = 16, circle_number_size: list = [12, 12, 12]):
    plt.figure(figsize=(4,4))
    out = venn2((dl_set, cnc_set), 
                (dl_name, cnc_name),
                set_colors=('silver', 'silver'), )
                # alpha = 0.8)
    venn2_circles((dl_set, cnc_set), 
                linestyle='-', 
                linewidth=1, 
                color='darkgrey')
    for text in out.set_labels:
        text.set_fontsize(circle_name_size)
    for i, text in enumerate(out.subset_labels):
        text.set_fontsize(circle_number_size[i])
    if save:
        plt.savefig(save_dir, dpi=50, bbox_inches='tight')
