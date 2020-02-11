import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

PATH_FILE_RISULTATI_PER_CASCADE = "../../Risultati/Percentili/Percentili_Results_Per_Cascade.csv"
PATH_FILE_GRAFICI_PER_CASCADE = "../../Risultati/Percentili/Plots/Percentili_Results_Per_Cascade.pdf"

FIELD_JACCARD_CASCADE = ['original_tweet_id', 'n_retweets', '25_outlier_retweet_perc_mean', '25_outlier_retweet_perc_mode', '25_outlier_retweet_perc_median', '25_outlier_retweet_perc_std', '25_outlier_retweet_perc_skw', '25_outlier_retweet_perc_kur', '25_outlier_retweet_perc_max', '5_outlier_retweet_perc_mean', '5_outlier_retweet_perc_mode', '5_outlier_retweet_perc_median', '5_outlier_retweet_perc_std', '5_outlier_retweet_perc_skw', '5_outlier_retweet_perc_kur', '5_outlier_retweet_perc_max', '25_max_lvl', '5_max_lvl', 'elapsed_time']

#Recuperiamo i risultati per livello dei percentili
df = pd.read_csv(PATH_FILE_RISULTATI_PER_CASCADE)

#Calcolo dei grafici
ax_25_perc_mean = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[2], style = 'o')
ax_25_perc_mode = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[3], style = 'o')
ax_25_perc_median = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[4], style = 'o')
ax_25_perc_std = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[5], style = 'o')
ax_25_perc_skw = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[6], style = 'o')
ax_25_perc_kur = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[7], style = 'o')
ax_25_perc_max = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[8], style = 'o')
ax_5_perc_mean = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[9], style = 'o')
ax_5_perc_mode = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[10], style = 'o')
ax_5_perc_median = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[11], style = 'o')
ax_5_perc_std = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[12], style = 'o')
ax_5_perc_skw = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[13], style = 'o')
ax_5_perc_kur = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[14], style = 'o')
ax_5_perc_max = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[15], style = 'o')
ax_25_max_lvl = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[16], style = 'o')
ax_5_max_lvl = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[17], style = 'o')
ax_elapsed_time = df.plot(x = 'n_retweets', y = FIELD_JACCARD_CASCADE[18], style = 'o')

#Recuperiamo le figure
figs = []
figs.append(ax_25_perc_mean.get_figure())
figs.append(ax_25_perc_mode.get_figure())
figs.append(ax_25_perc_median.get_figure())
figs.append(ax_25_perc_std.get_figure())
figs.append(ax_25_perc_skw.get_figure())
figs.append(ax_25_perc_kur.get_figure())
figs.append(ax_25_perc_max.get_figure())
figs.append(ax_5_perc_mean.get_figure())
figs.append(ax_5_perc_mode.get_figure())
figs.append(ax_5_perc_median.get_figure())
figs.append(ax_5_perc_std.get_figure())
figs.append(ax_5_perc_skw.get_figure())
figs.append(ax_5_perc_kur.get_figure())
figs.append(ax_5_perc_max.get_figure())
figs.append(ax_25_max_lvl.get_figure())
figs.append(ax_5_max_lvl.get_figure())
figs.append(ax_elapsed_time.get_figure())

#Salviamo su file
pp = PdfPages(PATH_FILE_GRAFICI_PER_CASCADE)
for fig in figs:
    fig.savefig(pp, format='pdf')
pp.close()