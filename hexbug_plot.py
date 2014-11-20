import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def plot_actual_vs_prediction(prediction=[], actual=[], err_fn=None):
    plt.title("Hexbug Locations", fontsize=18, y=1.1)
    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    plt.xlim(-1,max(zip(*prediction)[0]+zip(*actual)[0])*1.1)
    plt.ylim(max(zip(*prediction)[1]+zip(*actual)[1])*1.1, -1)
    prediction_handle = ax.scatter(*zip(*prediction), color='blue', alpha=.5)
    actual_handle = ax.scatter(*zip(*actual), color='green', alpha=.5)
    
    #Just need a dummy element for the legend
    extra = Rectangle((0, 0), 0, 0, fc="w", fill=False, edgecolor='none', linewidth=0)
    err_str = 'N/A'
    if err_fn:
        err_str = str(err_fn(prediction,actual))
    plt.legend([prediction_handle, actual_handle, extra], ['Predicted Locations', 'Actual Position', "L2 Error: " + err_str ], loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
    plt.show()   