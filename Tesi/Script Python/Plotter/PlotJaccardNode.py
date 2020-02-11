import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

PATH_FILE_RISULTATI = "../../Risultati/Jaccard_Node/Jaccard_Node_Results.csv"
PATH_FILE_GRAFICI = "../../Risultati/Jaccard_Node/Plots/Jaccard_Node_Plots.pdf"

#Recuperiamo i risultati per nodo degli indici relativi a Jaccard
df = pd.read_csv(PATH_FILE_RISULTATI)

#Calcolo dei grafici
ALPHA = 0.3

ax_mean = df.plot(x = 'n_retweets', y = 'usr_diff_mean', style = 'o', alpha = ALPHA)
ax_mode = df.plot(x = 'n_retweets', y = 'usr_diff_mode', style = 'o', alpha = ALPHA)
ax_median = df.plot(x = 'n_retweets', y = 'usr_diff_median', style = 'o', alpha = ALPHA)
ax_std = df.plot(x = 'n_retweets', y = 'usr_diff_std', style = 'o', alpha = ALPHA)
ax_skw = df.plot(x = 'n_retweets', y = 'usr_diff_skw', style = 'o', alpha = ALPHA)
ax_kur = df.plot(x = 'n_retweets', y = 'usr_diff_kur', style = 'o', alpha = ALPHA)
ax_time = df.plot(x = 'n_retweets', y = 'elapsed_time', style = 'o', alpha = ALPHA)

#Recuperiamo le figure
figs = []
figs.append(ax_mean.get_figure())
figs.append(ax_mode.get_figure())
figs.append(ax_median.get_figure())
figs.append(ax_std.get_figure())
figs.append(ax_skw.get_figure())
figs.append(ax_kur.get_figure())
figs.append(ax_time.get_figure())

#Salviamo su file
pp = PdfPages(PATH_FILE_GRAFICI)
for fig in figs:
    fig.savefig(pp, format='pdf')
pp.close()