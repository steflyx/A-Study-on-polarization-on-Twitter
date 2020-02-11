import sys
sys.path.append("../Utilities")

import pandas as pd
from scipy import stats
import csv

PATH_FILE_RESULTS_JACCARD_LEVEL = "../../Risultati/Jaccard_Level/Jaccard_Level_Results.csv"
PATH_FILE_METRICS = "../../dataset/Dataset formato CSV/metrics.csv"
PATH_FILE_RESULTS = "../../Risultati/Linear_Fit/Linear_Fit_Results.csv"

FIELD_LINEAR_FIT = ['original_tweet_id', 'lvl_usr_diff_slope', 'lvl_usr_diff_gof', 'lvl_usr_diff_intercept']

#Apriamo i risultati ottenuti precedentemente sulle cascate, divisi per livelli
pd_results = pd.read_csv(PATH_FILE_RESULTS_JACCARD_LEVEL)

with open(PATH_FILE_METRICS, encoding = "utf8") as file_metrics, open(PATH_FILE_RESULTS, 'w', newline = '') as file_results:
    reader_metrics = csv.DictReader(file_metrics)
    writer_results = csv.DictWriter(file_results, fieldnames = FIELD_LINEAR_FIT)
    writer_results.writeheader()
    
    row_counter = 0
    
    for row in reader_metrics:
        
        #Recuperiamo la lista delle medie, ordinate a partire dal livello più basso
        mean_list = list(pd_results.loc[(pd_results["original_tweet_id"] == int(row["original_tweet_id"])) & (pd_results['num_level'] != 1000)].sort_values("num_level", ascending = True)["lvl_usr_diff_mean"])
        
        #Non consideriamo le cascate troppo piccole o problematiche
        if not mean_list or len(mean_list) < 2:
            continue
        
        #Generiamo un array di numeri consecutivi da 1 al numero dei livelli
        x_axis = list(map(lambda x: x + 1, list(range(len(mean_list)))))
        
        #Effettuiamo il fit lineare
        slope, intercept, rvalue, pvalue, stderr = stats.linregress(x_axis, mean_list)            
        
        #Scriviamo i risultati
        writer_results.writerow({'original_tweet_id': row['original_tweet_id'], 'lvl_usr_diff_slope': slope, 'lvl_usr_diff_gof': rvalue, 'lvl_usr_diff_intercept': intercept})    
        
        row_counter += 1