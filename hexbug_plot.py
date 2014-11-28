import warnings
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from box_world import box_bounds

def plot_actual_vs_prediction(actual, prediction, orig_preceding=[], smoothed_preceding=[], err_fn=None):
    plt.title("Hexbug Locations", fontsize=18, y=1.1)
    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    bounds = box_bounds()
    margin = 20
    plt.xlim(bounds['min_x'] - margin, bounds['max_x'] + margin)
    plt.ylim(bounds['min_y'] - margin, bounds['max_y'] + margin)
    given_handle = ax.scatter(*zip(*orig_preceding), color='black', alpha=.5)
    smoothed_handle = ax.scatter(*zip(*smoothed_preceding), color='orange', alpha=.5)
    prediction_handle = ax.scatter(*zip(*prediction), color='blue', alpha=.5)
    actual_handle = ax.scatter(*zip(*actual), color='green', alpha=.5)

    #Just need a dummy element for the legend
    extra = Rectangle((0, 0), 0, 0, fc="w", fill=False, edgecolor='none', linewidth=0)
    err_str = 'N/A'
    if err_fn:
        err_str = str(err_fn(prediction,actual))
    plt.legend(
        [actual_handle, prediction_handle, given_handle, smoothed_handle, extra],
        ['Actual Position', 'Predicted Locations', 'Given points', 'Smoothed points', "L2 Error: " + err_str ],
        loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=3
    )
    set_layout(plt)
    plt.show()

def set_layout(plt):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        plt.tight_layout(rect=(0, .13, 1, 1.02))
