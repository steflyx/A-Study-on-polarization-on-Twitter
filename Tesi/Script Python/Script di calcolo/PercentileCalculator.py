import sys
sys.path.append("../Utilities")

import numpy as np
import pandas as pd
from RetweetersHandler import get_retweets_per_level, get_retweet_ratio
import FollowingHandler
import csv
import time

PATH_FILE_METRICS = "../../dataset/Dataset formato CSV/metrics.csv"
PATH_FILE_RESULTS_PER_LEVEL = "../../Risultati/Percentili/Percentili_Results_Per_Level.csv"
PATH_FILE_RESULTS_PER_CASCADE = "../../Risultati/Percentili/Percentili_Results_Per_Cascade.csv"

FIELDNAMES_PER_CASCADE = ['original_tweet_id', 'n_retweets', '25_outlier_retweet_perc_mean', '25_outlier_retweet_perc_mode', '25_outlier_retweet_perc_median', '25_outlier_retweet_perc_std', '25_outlier_retweet_perc_skw', '25_outlier_retweet_perc_kur', '25_outlier_retweet_perc_max', '5_outlier_retweet_perc_mean', '5_outlier_retweet_perc_mode', '5_outlier_retweet_perc_median', '5_outlier_retweet_perc_std', '5_outlier_retweet_perc_skw', '5_outlier_retweet_perc_kur', '5_outlier_retweet_perc_max', '25_max_lvl', '5_max_lvl', 'elapsed_time']
FIELDNAMES_PER_LEVEL = ['original_tweet_id', 'num_level', '25_outlier', '5_outlier', '25_outlier_perc', '5_outlier_perc']

following_handler = FollowingHandler.FollowingHasher()

#Calcola Jaccard fra i due array 'first' e 'second'
def get_Jaccard(first, second):
            
    #Si usa set() per rendere il calcolo più efficiente rispetto all'utilizzo di liste
    return len(set(first) & (set(second)))/(len(first) + len(second) - len(set(first) & (set(second)))) if first is not None and second is not None else None

#Calcola gli indici di jaccard e i percentili 25 e 5 divisi per livvello
#Gli utenti per cui non sono presenti following sono marcati con -1
def get_indexes_and_percentili_per_level(cascade, author_following):
    
    #Calcoliamo gli indici di jaccard e i percentili divisi per livello
    jaccard_indexes_per_level = []
    percentile_per_level = []
        
    for level in cascade:
            
        jaccard_list = []
            
        #Calcoliamo Jaccard per ogni utente del livello
        for user in level:
            jaccard_index = get_Jaccard(author_following, following_handler.get_following(str(user)))
                
            #Indichiamo con -1 gli utenti per cui non abbiamo i following (verranno esclusi dal calcolo del percentile)
            if jaccard_index is None:
                jaccard_list.append(-1)
            else:
                jaccard_list.append(jaccard_index)
            
        #Calcolo dei percentili: np.percentile restituisce il valore al di sotto del quale si trova l'x% dell'array (x secondo parametro)
        percentile_25 = np.percentile(list(filter(lambda x: x != -1, jaccard_list)), 25)
        percentile_5 = np.percentile(list(filter(lambda x: x != -1, jaccard_list)), 5)
            
        percentile_per_level.append([percentile_25, percentile_5])
        jaccard_indexes_per_level.append(jaccard_list)
        
    return jaccard_indexes_per_level, percentile_per_level

#Data una cascata e i valori di jaccard e dei percentili divisi per livelli, restituisce gli utenti, divisi per livelli, al di sotto dei rispettivi percentili
def get_users_under_percentile_per_level(cascade, jaccard_indexes_per_level, percentile_per_level):
    
    #Individuiamo gli utenti di ogni livello che si trovano al di sotto della soglia del percentile
    num_level = 0        
    users_target_per_level_percentile_25 = [] 
    users_target_per_level_percentile_5 = []
    
    for level in cascade:
            
        #Saltiamo la sorgente
        if num_level == 0:
            num_level += 1
            continue
            
        #Otteniamo i risultati di Jaccard e dei percentili associati a questo livello
        jaccard_indexes = jaccard_indexes_per_level[num_level]
        percentile_25 = percentile_per_level[num_level][0]
        percentile_5 = percentile_per_level[num_level][1]
        
        #Individuiamo gli utenti che sono al di sotto dei percentili
        user_percentile_25 = [] 
        user_percentile_5 = []
            
        for i in range(len(level)):
                
            if jaccard_indexes[i] != -1 and jaccard_indexes[i] <= percentile_25:
                user_percentile_25.append(level[i])
                if jaccard_indexes[i] <= percentile_5:
                    user_percentile_5.append(level[i])
                    
        users_target_per_level_percentile_25.append(user_percentile_25)
        users_target_per_level_percentile_5.append(user_percentile_5)
        
        num_level += 1
        
    return users_target_per_level_percentile_25, users_target_per_level_percentile_5
            
#Calcola e scrive i risultati relativi ad una riga
def write_results_per_cascade(writer, ratio_level_percentile_25, ratio_level_percentile_5, tweet_id, start_time, n_retweets):
    
    if ratio_level_percentile_25 and ratio_level_percentile_5:
    
        #Calcoliamo i risultati per cascata
        max_25 = max(ratio_per_level_percentile_25)
        max_5 = max(ratio_per_level_percentile_5)
            
        lvl_max_25 = ratio_per_level_percentile_25.index(max_25) + 1 #L'array salta la sorgente
        lvl_max_5 = ratio_per_level_percentile_5.index(max_5) + 1
            
        pd_ratio_per_level_percentile_25 = pd.DataFrame(ratio_per_level_percentile_25)
        pd_ratio_per_level_percentile_5 = pd.DataFrame(ratio_per_level_percentile_5)
            
        #Gli indici da calcolare sono nell'ordine: media, moda, mediano, deviazione standard, skewness, kurtosis
        mean_25 = float(pd_ratio_per_level_percentile_25.mean())
        mode_25 = float(pd_ratio_per_level_percentile_25.mode().iloc[0]) #Possono esserci più mode
        median_25 = float(pd_ratio_per_level_percentile_25.median())
        std_25 = float(pd_ratio_per_level_percentile_25.std())
        skewness_25 = float(pd_ratio_per_level_percentile_25.skew())
        kurtosis_25 = float(pd_ratio_per_level_percentile_25.kurt())
            
        mean_5 = float(pd_ratio_per_level_percentile_5.mean())
        mode_5 = float(pd_ratio_per_level_percentile_5.mode().iloc[0]) #Possono esserci più mode
        median_5 = float(pd_ratio_per_level_percentile_5.median())
        std_5 = float(pd_ratio_per_level_percentile_5.std())
        skewness_5 = float(pd_ratio_per_level_percentile_5.skew())
        kurtosis_5 = float(pd_ratio_per_level_percentile_5.kurt())
    
        end = time.time()
        elapsed_time = end - start
            
        #Scriviamo i risultati
        writer.writerow({'original_tweet_id': tweet_id, 'n_retweets': n_retweets,'25_outlier_retweet_perc_mean': mean_25, '25_outlier_retweet_perc_mode': mode_25, '25_outlier_retweet_perc_median': median_25, '25_outlier_retweet_perc_std': std_25, '25_outlier_retweet_perc_skw': skewness_25, '25_outlier_retweet_perc_kur': kurtosis_25, '25_outlier_retweet_perc_max': max_25, '5_outlier_retweet_perc_mean': mean_5, '5_outlier_retweet_perc_mode': mode_5, '5_outlier_retweet_perc_median': median_5, '5_outlier_retweet_perc_std': std_5, '5_outlier_retweet_perc_skw': skewness_5, '5_outlier_retweet_perc_kur': kurtosis_5, '5_outlier_retweet_perc_max': max_5, '25_max_lvl': lvl_max_25, '5_max_lvl': lvl_max_5, 'elapsed_time': elapsed_time})

    #L'array dei percentili può essere vuoto in alcuni casi
    else:
        
        end = time.time()
        elapsed_time = end - start
        
        writer.writerow({'original_tweet_id': tweet_id, '25_outlier_retweet_perc_mean': -1, '25_outlier_retweet_perc_mode': -1, '25_outlier_retweet_perc_median': -1, '25_outlier_retweet_perc_std': -1, '25_outlier_retweet_perc_skw': -1, '25_outlier_retweet_perc_kur': -1, '25_outlier_retweet_perc_max': -1, '5_outlier_retweet_perc_mean': -1, '5_outlier_retweet_perc_mode': -1, '5_outlier_retweet_perc_median': -1, '5_outlier_retweet_perc_std': -1, '5_outlier_retweet_perc_skw': -1, '5_outlier_retweet_perc_kur': -1, '5_outlier_retweet_perc_max': -1, '25_max_lvl': -1, '5_max_lvl': -1, 'elapsed_time': elapsed_time})



with open(PATH_FILE_METRICS, encoding = "utf8") as file_metrics, open(PATH_FILE_RESULTS_PER_LEVEL, 'w', newline = '') as file_results_per_level, open(PATH_FILE_RESULTS_PER_CASCADE, 'w', newline = '') as file_results_per_cascade:
    reader_metrics = csv.DictReader(file_metrics)
    writer_results_per_level = csv.DictWriter(file_results_per_level, fieldnames = FIELDNAMES_PER_LEVEL)
    writer_results_per_cascade = csv.DictWriter(file_results_per_cascade, fieldnames = FIELDNAMES_PER_CASCADE)
    writer_results_per_level.writeheader()
    writer_results_per_cascade.writeheader()
    
    row_counter = 0
    
    for row in reader_metrics:
        
        #Calcolo del tempo impiegato per una cascata
        start = time.time()
        
        #Calcoliamo la cascata divisa per livelli        
        cascade = get_retweets_per_level(row['original_tweet_id'])
        
        #Controlliamo se l'autore del tweet è presente nel database
        if cascade[0][0] == -1:
            continue
        
        #Calcoliamo i following dell'autore per accelerare i tempi successivamente
        author_following = following_handler.get_following(str(cascade[0][0]))
        if author_following is None:
            print("Nessun following per autore cascata " + str(row_counter))
            row_counter += 1
            continue
        
        #Calcoliamo gli indici di Jaccard e i percentili divisi per livello
        jaccard_indexes_per_level, percentile_per_level = get_indexes_and_percentili_per_level(cascade, author_following)
        
        #Calcoliamo gli utenti che si trovano al di sotto dei percentili
        users_target_per_level_percentile_25, users_target_per_level_percentile_5 = get_users_under_percentile_per_level(cascade, jaccard_indexes_per_level, percentile_per_level)
        
        #Calcoliamo i rapporti fra i retweet ottenuti dagli utenti sotto i percentili e quelli ottenuti dagli utenti del corrispondente livello        
        ratio_per_level_percentile_25 = get_retweet_ratio(users_target_per_level_percentile_25, row['original_tweet_id'])
        ratio_per_level_percentile_5 = get_retweet_ratio(users_target_per_level_percentile_5, row['original_tweet_id'])
        
        #Scriviamo i risultati per livello
        num_level = 0
        for i in range(len(cascade)):
            
            #Sorgente
            if num_level == 0:
                num_level += 1
                continue
            
            #User sparsi
            if num_level == len(cascade) - 1: 
                num_level = 1000
            
            try:
                writer_results_per_level.writerow({'original_tweet_id': row['original_tweet_id'], 'num_level': num_level, '25_outlier': percentile_per_level[i][0], '5_outlier': percentile_per_level[i][1], '25_outlier_perc': ratio_per_level_percentile_25[i-1], '5_outlier_perc': ratio_per_level_percentile_5[i-1]})
            except IndexError:
                writer_results_per_level.writerow({'original_tweet_id': row['original_tweet_id'], 'num_level': num_level, '25_outlier': percentile_per_level[i][0], '5_outlier': percentile_per_level[i][1], '25_outlier_perc': -1, '5_outlier_perc': -1})
            
            num_level += 1
        
        #Calcoliamo e scriviamo i risultati per cascata
        write_results_per_cascade(writer_results_per_cascade, ratio_per_level_percentile_25, ratio_per_level_percentile_5, row['original_tweet_id'], start, row['n_retweets'])
        
        end = time.time()
        elapsed_time = end - start
        
        print("Completata cascata " + str(row_counter) + " in " + str(elapsed_time) + " secondi")
        
        row_counter += 1