import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

PATH_FILE_RISULTATI = "../../Risultati/Jaccard_Level/Jaccard_Level_Results.csv"
PATH_FILE_GRAFICI = "../../Risultati/Jaccard_Level/Plots/Jaccard_Level_Plots.pdf"

FIELD_JACCARD_LEVEL = ['original_tweet_id', 'lvl_usr_diff_mean', 'lvl_usr_diff_mode', 'lvl_usr_diff_median', 'lvl_usr_diff_std', 'lvl_usr_diff_skw', 'lvl_usr_diff_kur', 'num_level']

ALPHA = 0.2

#Recuperiamo i risultati per nodo degli indici relativi a Jaccard
df = pd.read_csv(PATH_FILE_RISULTATI)

#Per facilitare la comprensione del grafico, i nodi sparsi vengono indicati con -1
df['num_level'] = df['num_level'].apply(lambda x: -1 if x == 1000 else x)

#Calcolo dei grafici
ax_mean = df.plot(x = 'num_level', y = FIELD_JACCARD_LEVEL[1], style = 'o', alpha = ALPHA)
ax_mode = df.plot(x = 'num_level', y = FIELD_JACCARD_LEVEL[2], style = 'o', alpha = ALPHA)
ax_median = df.plot(x = 'num_level', y = FIELD_JACCARD_LEVEL[3], style = 'o', alpha = ALPHA)
ax_std = df.plot(x = 'num_level', y = FIELD_JACCARD_LEVEL[4], style = 'o', alpha = ALPHA)
ax_skw = df.plot(x = 'num_level', y = FIELD_JACCARD_LEVEL[5], style = 'o', alpha = ALPHA)
ax_kur = df.plot(x = 'num_level', y = FIELD_JACCARD_LEVEL[6], style = 'o', alpha = ALPHA)

#Recuperiamo le figure
figs = []
figs.append(ax_mean.get_figure())
figs.append(ax_mode.get_figure())
figs.append(ax_median.get_figure())
figs.append(ax_std.get_figure())
figs.append(ax_skw.get_figure())
figs.append(ax_kur.get_figure())

#Salviamo su file
pp = PdfPages(PATH_FILE_GRAFICI)
for fig in figs:
    fig.savefig(pp, format='pdf')
pp.close()