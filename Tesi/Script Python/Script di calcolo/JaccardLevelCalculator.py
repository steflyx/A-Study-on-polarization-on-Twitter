import sys
sys.path.append("../Utilities")

from RetweetersHandler import get_retweets_per_level
import FollowingHandler
import csv
import pandas as pd
import time

PATH_FILE_METRICS = "../../dataset/Dataset formato CSV/metrics.csv"
PATH_FILE_RESULTS = "../../Risultati/Jaccard_Level/Jaccard_Level_Results.csv"
PATH_FILE_RESULTS_PER_CASCADE = "../../Risultati/Jaccard_Level/Jaccard_Level_Results_Per_Cascade.csv"

FIELD_JACCARD_LEVEL = ['original_tweet_id', 'lvl_usr_diff_mean', 'lvl_usr_diff_mode', 'lvl_usr_diff_median', 'lvl_usr_diff_std', 'lvl_usr_diff_skw', 'lvl_usr_diff_kur', 'num_level']

following_handler = FollowingHandler.FollowingHasher()

#Calcola Jaccard fra i due array 'first' e 'second'
def get_Jaccard(first, second):
            
    #Si usa set() per rendere il calcolo più efficiente rispetto all'utilizzo di liste
    return len(set(first) & (set(second)))/(len(first) + len(second) - len(set(first) & (set(second)))) if first is not None and second is not None else None


with open(PATH_FILE_METRICS, encoding = "utf8") as file_metrics, open(PATH_FILE_RESULTS, 'w', newline = '') as file_results, open(PATH_FILE_RESULTS_PER_CASCADE, 'w', newline = '') as file_results_per_cascade:
    metrics = csv.DictReader(file_metrics)
    writer_results = csv.DictWriter(file_results, fieldnames = FIELD_JACCARD_LEVEL)
    writer_results.writeheader()
    
    row_counter = 0
    
    for row in metrics:

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
        
        #Calcoliamo gli indici di jaccard divisi per livello
        jaccard_indexes_per_level = []
        
        for level in cascade:
            
            jaccard_list = []
            
            #Calcoliamo Jaccard per ogni utente del livello
            for user in level:
                jaccard_index = get_Jaccard(author_following, following_handler.get_following(str(user)))
                
                if jaccard_index is None:
                    continue
                else:
                    jaccard_list.append(jaccard_index)
                    
            jaccard_indexes_per_level.append(jaccard_list)
            
        #Calcoliamo i vari indici sempre divisi per livello
        num_level = 0        
        
        for level in jaccard_indexes_per_level:
            
            #Saltiamo il livello della sorgente e i livelli troppo piccoli per poterci calcolare gli indici statistici
            if num_level == 0 or len(level) < 2:
                num_level += 1
                continue

            #Distinguiamo il livello degli indici sparsi con 1000
            if num_level == len(jaccard_indexes_per_level) - 1: 
                num_level = 1000
            
            pd_level = pd.DataFrame(level)
            
            #Gli indici da calcolare sono nell'ordine: media, moda, mediano, deviazione standard, skewness, kurtosis
            mean = float(pd_level.mean())
            mode = float(pd_level.mode().iloc[0]) #Possono esserci più mode
            median = float(pd_level.median())
            std = float(pd_level.std())
            skewness = float(pd_level.skew())
            kurtosis = float(pd_level.kurt())
            
            #Scriviamo il risultato
            writer_results.writerow({'original_tweet_id': row['original_tweet_id'], 'lvl_usr_diff_mean': mean, 'lvl_usr_diff_mode': mode, 'lvl_usr_diff_median': median, 'lvl_usr_diff_std': std, 'lvl_usr_diff_skw': skewness, 'lvl_usr_diff_kur': kurtosis, 'num_level': num_level})
            
            print("Completato il livello " + str(num_level))
            print("Media di " + str(mean))
            print("Moda di " + str(mode))
            print("Mediano di " + str(median))
            print("Std di " + str(std))
            print("Skewness di " + str(skewness))
            print("Kurtosis di " + str(kurtosis))
            
            num_level += 1
        
        #Calcolo del tempo impiegato per una cascata
        end = time.time()
        elapsed_time = end - start
        
        print("Completata cascata " + row['original_tweet_id'] + " (" + str(row_counter) + ") in " + str(elapsed_time) + " secondi")
        
        row_counter += 1