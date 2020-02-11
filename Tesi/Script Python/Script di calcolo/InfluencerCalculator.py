import sys
sys.path.append("../Utilities")

import pandas as pd
import RetweetersHandler
import time
import csv

PATH_FILE_USERS = "../../dataset/Dataset formato CSV/users.csv"
PATH_FILE_METRICS = "../../dataset/Dataset formato CSV/metrics.csv"
PATH_FILE_METRICS_PARZIALI_INFLUENCER = "../../Risultati/Influence/Influence_Results.csv"
FIELD_INFLUENCER = ['original_tweet_id', 'influencer_mean', 'influencer_mode', 'influencer_median', 'influencer_std', 'influencer_skw', 'influencer_kur', 'n_retweeter', 'elapsed_time']

users_data = pd.read_csv(PATH_FILE_USERS) 
cascades_id = pd.read_csv(PATH_FILE_METRICS)["original_tweet_id"]

#Ritorna il rapporto follower/following dell'utente specificato. Se l'utente non esiste o non ha following ritorna None
#NOTA: per controllare se l'utente non ha following usiamo la funzione 'any' perché != 0 dà errore
def get_ratio_follower_following(user_id):
    
    user_row = users_data.loc[users_data["id"] == int(user_id)]    
    return user_row["followers_count"]/user_row["friends_count"] if not user_row.empty and user_row["friends_count"].any() else None


with open(PATH_FILE_METRICS_PARZIALI_INFLUENCER, 'w', newline = '') as file_results:
    writer_results = csv.DictWriter(file_results, fieldnames = FIELD_INFLUENCER)
    writer_results.writeheader()
    
    #Si esegue un ciclo for, analizzando una cascata per volta
    for row in cascades_id:    
        
        #Calcolo del tempo di esecuzione
        start = time.time()
        
        #Recuperiamo autore e retweet della cascata
        author = RetweetersHandler.get_author(str(row))
        retweets = RetweetersHandler.get_retweets(str(row))
        
        #Creiamo un array in cui andiamo a salvare i rapporti di ogni utente coinvolto nella cascata (autore + retweeter)
        ratio_array = [get_ratio_follower_following(author)]
        for item in retweets:        
            ratio_array.append(get_ratio_follower_following(item['retweeter_user_id']))
        
        #Filtriamo l'array dei valori nulli e convertiamo tutti gli elementi in float
        ratio_array = list(filter(lambda x: x is not None, ratio_array))
        ratio_array = list(map(lambda x: float(x), ratio_array))
        
        #Controlliamo se l'array è vuoto
        if not ratio_array:
            print('Array vuoto')
            continue
        
        #Convertiamo l'array in un dataframe Pandas
        pd_ratio_array = pd.DataFrame(ratio_array)
        
        #Gli indici da calcolare sono nell'ordine: media, moda, mediano, deviazione standard, skewness, kurtosis
        mean = float(pd_ratio_array.mean())    
        mode = float(pd_ratio_array.mode().iloc[0]) #Possono esserci più mode
        median = float(pd_ratio_array.median())
        std = float(pd_ratio_array.std())
        skewness = float(pd_ratio_array.skew())
        kurtosis = float(pd_ratio_array.kurt())
        
        #Calcolo del tempo di esecuzione
        end = time.time()
        elapsed_time = end - start
        
        #Scrittura dei risultati sul file csv
        writer_results.writerow({'original_tweet_id': row, 'influencer_mean': mean, 'influencer_mode': mode, 'influencer_median': median, 'influencer_std': std, 'influencer_skw': skewness, 'influencer_kur': kurtosis, 'n_retweeter': len(ratio_array), 'elapsed_time': elapsed_time})
        
        print("Media = " + str(mean))
        print("Moda = " + str(mode))
        print("Mediano = " + str(median))
        print("Deviazione standard = " + str(std))
        print("Skewness = " + str(skewness))
        print("Kurtosis = " + str(kurtosis))
        print("Tempo di calcolo = " + str(elapsed_time))