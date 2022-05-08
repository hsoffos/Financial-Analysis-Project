import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font='Franklin Gothic Book',
        rc={
        'axes.axisbelow': False,
        'axes.edgecolor': 'lightgrey',
        'axes.facecolor': 'None',
        'axes.grid': False,
        'axes.labelcolor': 'dimgrey',
        'axes.spines.right': False,
        'axes.spines.top': False,
        'figure.facecolor': 'white',
        'lines.solid_capstyle': 'round',
        'patch.edgecolor': 'w',
        'patch.force_edgecolor': True,
        'text.color': 'dimgrey',
        'xtick.bottom': False,
        'xtick.color': 'dimgrey',
        'xtick.direction': 'out',
        'xtick.top': False,
        'ytick.color': 'dimgrey',
        'ytick.direction': 'out',
        'ytick.left': False,
        'ytick.right': False
        })
sns.set_context("notebook",rc=
                {"font.size":16,
                 "axes.titlesize":20,
                 "axes.labelsize":18})

CB91_Blue, CB91_Pink = '#2CBDFE', '#F3A0F2'
CB91_Green, CB91_Amber = '#47DBCD', '#F5B14C'
CB91_Purple, CB91_Violet = '#9D2EC5', '#661D98'

color_list = [CB91_Blue, CB91_Pink,
              CB91_Green, CB91_Amber,
              CB91_Purple, CB91_Violet]

plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)