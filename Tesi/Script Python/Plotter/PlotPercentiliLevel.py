import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

PATH_FILE_RISULTATI_PER_LEVEL = "../../Risultati/Percentili/Percentili_Results_Per_Level.csv"
PATH_FILE_GRAFICI_PER_LEVEL = "../../Risultati/Percentili/Plots/Percentili_Results_Per_Level.pdf"

FIELD_JACCARD_LEVEL = ['original_tweet_id', 'num_level', '25_outlier', '5_outlier', '25_outlier_perc', '5_outlier_perc']

#Recuperiamo i risultati per livello dei percentili
df = pd.read_csv(PATH_FILE_RISULTATI_PER_LEVEL)

#Per facilitare la comprensione del grafico, i nodi sparsi vengono indicati con -1
df['num_level'] = df['num_level'].apply(lambda x: -1 if x == 1000 else x)

#Calcolo dei grafici
ALPHA = 0.3

ax_25 = df.plot(x = 'num_level', y = FIELD_JACCARD_LEVEL[2], style = 'o', alpha = ALPHA)
ax_5 = df.plot(x = 'num_level', y = FIELD_JACCARD_LEVEL[3], style = 'o', alpha = ALPHA)
ax_25_perc = df.plot(x = 'num_level', y = FIELD_JACCARD_LEVEL[4], style = 'o', ylim = (-0.05, 1.05), alpha = ALPHA) #Elimina i valori nulli (indicati con -1)
ax_5_perc = df.plot(x = 'num_level', y = FIELD_JACCARD_LEVEL[5], style = 'o', ylim = (-0.05, 1.05), alpha = ALPHA)

#Recuperiamo le figure
figs = []
figs.append(ax_25.get_figure())
figs.append(ax_5.get_figure())
figs.append(ax_25_perc.get_figure())
figs.append(ax_5_perc.get_figure())

#Salviamo su file
pp = PdfPages(PATH_FILE_GRAFICI_PER_LEVEL)
for fig in figs:
    fig.savefig(pp, format='pdf')
pp.close()