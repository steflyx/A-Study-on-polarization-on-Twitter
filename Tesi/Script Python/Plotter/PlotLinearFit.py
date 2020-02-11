import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

PATH_FILE_PLOTS = "../../Risultati/Linear_Fit/Plots/Linear_Fit_Plots.pdf"
PATH_FILE_RESULTS_JACCARD_LEVEL = "../../Risultati/Jaccard_Level/Jaccard_Level_Results.csv"
PATH_FILE_RESULTS_LINEAR_FIT = "../../Risultati/Linear_Fit/Linear_Fit_Results.csv"

#Apriamo i risultati per livello
pd_results = pd.read_csv(PATH_FILE_RESULTS_JACCARD_LEVEL)

with open(PATH_FILE_RESULTS_LINEAR_FIT, encoding = "utf8") as file_linear_fit:
    reader_linear_fit = csv.DictReader(file_linear_fit)
    
    graphs = 0
    
    #Disegnamo 6 grafici: solo linee, solo curve, linee + punti, curve + punti, linee + curve, linee + curve + punti
    fig_lines, ax_lines = plt.subplots()
    plt.xlabel('Prova')
    plt.ylabel('ProvaY')
    
    
    fig_curves, ax_curves = plt.subplots()
    fig_lines_points, ax_lines_points = plt.subplots()
    fig_curves_points, ax_curves_points = plt.subplots()
    fig_lines_curves, ax_lines_curves = plt.subplots()
    fig_lines_curves_points, ax_lines_curves_points = plt.subplots()
    
    plt.xlabel('Prova')
    plt.ylabel('ProvaY')
    
    for row in reader_linear_fit:
        
        #Recuperiamo la lista delle medie, ordinate a partire dal livello più basso
        mean_list = list(pd_results.loc[(pd_results["original_tweet_id"] == int(row["original_tweet_id"])) & (pd_results['num_level'] != 1000)].sort_values("num_level", ascending = True)["lvl_usr_diff_mean"])
        
        #Non consideriamo le cascate troppo piccole o problematiche
        if not mean_list or len(mean_list) < 5:
            continue
        
        #Generiamo un array di numeri consecutivi da 1 al numero dei livelli
        x_axis = list(map(lambda x: x + 1, list(range(len(mean_list)))))
        
        #Recuperiamo le informazioni sul linear fitting
        slope = float(row['lvl_usr_diff_slope'])
        intercept = float(row['lvl_usr_diff_intercept'])
        
        #Tracciamo il grafico solo per i valori più significativi e solo per un limitato numero di cascate
        if len(x_axis) > 5 and graphs < 10:
            
            #Disegnamo le rette
            #line1 permette di ricavare alcune informazioni sul grafico. In particolare ci interessa il colore per riutilizzarlo dopo
            line1, = ax_lines.plot(np.array(x_axis), intercept + slope * np.array(x_axis), color = 'C' + str(graphs))
            line2, = ax_lines_points.plot(np.array(x_axis), intercept + slope * np.array(x_axis))
            line3, = ax_lines_curves.plot(np.array(x_axis), intercept + slope * np.array(x_axis))
            line4, = ax_lines_curves_points.plot(np.array(x_axis), intercept + slope * np.array(x_axis))
            line2.set_color(line1.get_color())
            line3.set_color(line1.get_color())
            line4.set_color(line1.get_color())

            #Disegnamo i punti            
            line2, = ax_lines_points.plot(x_axis, mean_list, marker = "o", linestyle = '')
            line3, = ax_curves_points.plot(x_axis, mean_list, marker = "o", linestyle = '')
            line4, = ax_lines_curves_points.plot(x_axis, mean_list, marker = "o", linestyle = '')
            line2.set_color(line1.get_color())
            line3.set_color(line1.get_color())
            line4.set_color(line1.get_color())
            
            #Calcoliamo le informazioni necessarie per disegnare il polinomio che unisce i punti
            coefficienti = np.polyfit(x_axis, mean_list, len(x_axis))
            polinomio = np.poly1d(coefficienti)
            linspace = np.linspace(1, len(x_axis))
            
            #Disegnamo il polinomio
            line2, = ax_curves.plot(linspace, polinomio(linspace), linestyle = ':')
            line3, = ax_curves_points.plot(linspace, polinomio(linspace), linestyle = ':')
            line4, = ax_lines_curves.plot(linspace, polinomio(linspace), linestyle = ':')
            line5, = ax_lines_curves_points.plot(linspace, polinomio(linspace), linestyle = ':')
            line2.set_color(line1.get_color())
            line3.set_color(line1.get_color())
            line4.set_color(line1.get_color())
            line5.set_color(line1.get_color())
            
            graphs += 1            
            
        if graphs >= 10:
            break
        
    
    #Salviamo i grafici
    #Recuperiamo le figure
    figs = []
    figs.append(fig_lines)
    figs.append(fig_curves)
    figs.append(fig_lines_points)
    figs.append(fig_curves_points)
    figs.append(fig_lines_curves)
    figs.append(fig_lines_curves_points)
    
    #Salviamo su file
    pp = PdfPages(PATH_FILE_PLOTS)
    for fig in figs:
        fig.savefig(pp, format='pdf')
    pp.close()
            
            