import sys
sys.path.append("../Utilities")

import FollowingHandler
import RetweetersHandler
import csv
import statistics
import time
import pandas as pd

PATH_FILE_METRICS_PARZIALI = "../../dataset/Dataset formato CSV/metrics_parziali.csv"
PATH_FILE_RISULTATI_JACCARD_NODO = "../../Risultati/Jaccard_Node/Jaccard_Node_Results.csv"

FIELD_JACCARD_NODO = ['original_tweet_id', 'usr_diff_mean', 'usr_diff_mode', 'usr_diff_median', 'usr_diff_std', 'usr_diff_skw', 'usr_diff_kur', 'n_retweets', 'elapsed_time']

following_handler = FollowingHandler.FollowingHasher()

#Calcola Jaccard fra i due array 'first' e 'second'
def get_Jaccard(first, second):
            
    #Si usa set() per rendere il calcolo più efficiente rispetto all'utilizzo di liste
    return len(set(first) & (set(second)))/(len(first) + len(second) - len(set(first) & (set(second)))) if first is not None and second is not None else None
    

with open(PATH_FILE_METRICS_PARZIALI, encoding = "utf8") as file_metrics, open(PATH_FILE_RISULTATI_JACCARD_NODO, 'w', newline = '') as file_risultati:
    reader_metrics = csv.reader(file_metrics)
    writer_results = csv.DictWriter(file_risultati, fieldnames = FIELD_JACCARD_NODO)
    writer_results.writeheader()
    
    row_counter = 0
    
    for row in reader_metrics:
        
        start = time.time()
        
        #Recuperiamo l'autore del tweet che ha originato la cascata
        author = RetweetersHandler.get_author(row[0])
        
        #Si controlla che si sia riuscito a trovare l'autore
        if author == -1:
            continue
        
        #Recuperiamo tutti i retweet che fanno parte della cascata
        retweets = RetweetersHandler.get_retweets(row[0])
        
        #Passiamo al calcolo dell'indice di Jaccard fra ogni utente della cascata e l'autore originale
        jaccard_list = []
        author_following = following_handler.get_following(str(author)) #Recuperiamo i following dell'autore una volta per tutte
        
        for tweet in retweets:
            
            jaccard_index = get_Jaccard(author_following, following_handler.get_following(str(tweet['retweeter_user_id'])))
            
            if jaccard_index is not None:
                jaccard_list.append(jaccard_index)
            
        #Calcolo di media, moda, mediano e deviazione standard
        mean = statistics.mean(jaccard_list)
        
        #Poiché è difficile che si possa trovare una moda significativa in un array di float,
        #valuto solo le prime cifre decimali, continuando ad approssimare fino a trovarne una
        mode = 0
        approx = 10000
        while mode == 0 and approx != 1:
            try:
                mode = statistics.mode(map(lambda x: int(x*approx), jaccard_list))/approx
            except statistics.StatisticsError:
                mode = 0
            approx /= 10
                    
        
        median = statistics.median(jaccard_list)        
        standard_deviation = statistics.pstdev(jaccard_list, mu = mean)
                
        
        #Conversione della lista in un DataFrame Pandas per il calcolo di skweness e Kurtosis
        pd_jaccard_list = pd.DataFrame(jaccard_list)
        
        #Calcolo Skewness e Kurtosis
        skewness = float(pd_jaccard_list.skew())
        kurtosis = float(pd_jaccard_list.kurt())       
        
        #Calcolo del tempo di elaborazione
        end = time.time()
        elapsed_time = end - start
        
        #Scrittura dei risultati
        writer_results.writerow({'original_tweet_id': row[0], 'usr_diff_mean': mean, 'usr_diff_mode': mode, 'usr_diff_median': median, 'usr_diff_std': standard_deviation, 'usr_diff_skw': skewness, 'usr_diff_kur': kurtosis, 'n_retweets': len(jaccard_list), 'elapsed_time': elapsed_time})
                
        print("Media di " + str(mean))
        print("Moda di " + str(mode))
        print("Mediano di " + str(median))
        print("Std di " + str(standard_deviation))
        print("Skewness di " + str(skewness))
        print("Kurtosis di " + str(kurtosis))
        print("Completata la riga " + str(row_counter) + " in " + str(elapsed_time) + " secondi; lunghezza: " + str(len(jaccard_list)))
        
        row_counter += 1