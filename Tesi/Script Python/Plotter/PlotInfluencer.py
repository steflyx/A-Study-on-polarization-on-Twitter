import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

PATH_FILE_RISULTATI = "../../Risultati/Influence/Influence_Results.csv"
PATH_FILE_GRAFICI = "../../Risultati/Influence/Plots/Ratio_Follower_Following_Plots.pdf"
FIELD_INFLUENCER = ['original_tweet_id', 'influencer_mean', 'influencer_mode', 'influencer_median', 'influencer_std', 'influencer_skw', 'influencer_kur', 'n_retweeter', 'elapsed_time']

#Recuperiamo i risultati riguardanti gli indici sulla distribuzione del rapporto follower/following
df = pd.read_csv(PATH_FILE_RISULTATI)

#Disegnamo i grafici
ALPHA = 0.3

ax_mean = df.plot(x = 'n_retweeter', y = FIELD_INFLUENCER[1], style = 'o', alpha = ALPHA)
ax_mean_zoom = df.plot(x = 'n_retweeter', y = FIELD_INFLUENCER[1], style = 'o', alpha = ALPHA, ylim = (0, 10))
ax_mean_zoom_2 = df.plot(x = 'n_retweeter', y = FIELD_INFLUENCER[1], style = 'o', alpha = ALPHA, ylim = (0, 2))
ax_mode = df.plot(x = 'n_retweeter', y = FIELD_INFLUENCER[2], style = 'o', alpha = ALPHA)
ax_mode_zoom = df.plot(x = 'n_retweeter', y = FIELD_INFLUENCER[2], style = 'o', alpha = ALPHA, ylim = (0, 5))
ax_median = df.plot(x = 'n_retweeter', y = FIELD_INFLUENCER[3], style = 'o', alpha = ALPHA)
ax_std = df.plot(x = 'n_retweeter', y = FIELD_INFLUENCER[4], style = 'o', alpha = ALPHA)
ax_std_zoom = df.plot(x = 'n_retweeter', y = FIELD_INFLUENCER[4], style = 'o', alpha = ALPHA, ylim = (0, 20))
ax_skw = df.plot(x = 'n_retweeter', y = FIELD_INFLUENCER[5], style = 'o', alpha = ALPHA)
ax_kur = df.plot(x = 'n_retweeter', y = FIELD_INFLUENCER[6], style = 'o', alpha = ALPHA)
ax_time = df.plot(x = 'n_retweeter', y = FIELD_INFLUENCER[8], style = 'o', alpha = ALPHA)

#Recuperiamo le figure
figs = []
figs.append(ax_mean.get_figure())
figs.append(ax_mean_zoom.get_figure())
figs.append(ax_mean_zoom_2.get_figure())
figs.append(ax_mode.get_figure())
figs.append(ax_mode_zoom.get_figure())
figs.append(ax_median.get_figure())
figs.append(ax_std.get_figure())
figs.append(ax_std_zoom.get_figure())
figs.append(ax_skw.get_figure())
figs.append(ax_kur.get_figure())
figs.append(ax_time.get_figure())

#Salviamo su file
pp = PdfPages(PATH_FILE_GRAFICI)
for fig in figs:
    fig.savefig(pp, format='pdf')
pp.close()