import csv
import pandas as pd

PATH_FILE_RETWEET_TREE = "../../dataset/Dataset formato CSV/retweets_tree.csv"
PATH_FILE_USER = "../../dataset/Dataset formato CSV/users.csv"
PATH_FILE_TWEET = "../../dataset/Dataset formato CSV/tweets.csv"
PATH_FILE_METRICS = "../../dataset/Dataset formato CSV/metrics.csv"

#Ritorna tutti i record della tabella "retweets_tree" che hanno per tweet originale 'tweet_id'
def get_retweets(tweet_id):
        
    result = []
        
    with open(PATH_FILE_RETWEET_TREE, encoding = "utf8") as retweets_tree_file:
        retweet_reader = csv.DictReader(retweets_tree_file)
            
        for row in retweet_reader:                
            if row['original_tweet_id'] == tweet_id:
                result.append(row)
                    
    return result
    
#Dato l'id di un tweet, ne ritorna l'id dell'autore
#NOTA: dei tweet in 'metrics' non si trovano corrispondenze per i tweet '874505164203413507' e '954449015210496001', i quali verranno gestiti separatamente
def get_author(tweet_id):
        
    if tweet_id in ['874505164203413507', '954449015210496001']:
        print("Hai inserito una delle due cascate non presenti in tabella")
        return -1
        
    with open(PATH_FILE_TWEET, encoding = "utf8") as tweet_file:
        tweet_reader = csv.DictReader(tweet_file)
            
        for row in tweet_reader:                
            if str(row['id']) == str(tweet_id):
                return row['user_id']
            
    return -1
        
#Ritorna una lista contenente gli utenti che hanno retwittato tweet_id, divisi per livelli
def get_retweets_per_level(tweet_id):
        
    tweet_id = int(tweet_id) #Serve per fare le query con pandas
    retweets_tree = pd.read_csv(PATH_FILE_RETWEET_TREE)
    levels = [[get_author(tweet_id)]] #Il livello 0 è l'utente iniziale
        
    #Si fa un ciclo sulla lista dei retweet, scendendo man mano di livello
    while True:
            
        #Questa query cerca i retweet relativi a tweet_id in cui l'utente retwittato è fra quelli dell'ultimo livello completato
        level = list(retweets_tree.loc[(retweets_tree["retweeted_user_id"].isin(levels[len(levels) - 1])) & (retweets_tree["original_tweet_id"] == tweet_id)]["retweeter_user_id"])
            
        #Per evitare loop, ci assicuriamo che un utente non abbia retwittato due volte lo stesso tweet (nel qual caso sarebbe già in un livello precedente)
        for row in levels:
            for item in level:
                if item in row:
                    level.remove(item)
            
        #Se non abbiamo trovato nuovi retweet, abbiamo terminato la cascata
        if not level:
            break
        else:
            levels.append(level)
            
    #Aggiungiamo un ultimo livello che racchiuderà gli utenti sparsi
    #NOTA: Questo livello sarà sempre presente, al più sarà vuoto
    levels.append(get_retweet_sparsi(tweet_id, retweets_tree))
        
    return levels

#Funzione che restituisce una lista contenente tutti i retweet sparsi relativi a 'tweet_id'
def get_retweet_sparsi(tweet_id, retweets_tree):
    
    #Recuperiamo i retweet sparsi di 'primo livello', cioè quelli che hanno NULL nel campo retweeted_user_id
    retweet_sparsi_primo_livello = list(retweets_tree.loc[(retweets_tree["retweeted_user_id"].isnull()) & (retweets_tree["original_tweet_id"] == tweet_id)]["retweeter_user_id"])
    
    #Cerchiamo poi i retweet dei retweet sparsi di primo livello, poi i retweet di questi ultimi e così via
    retweet_sparsi_totali = retweet_sparsi_secondo_livello = retweet_sparsi_primo_livello
    
    while retweet_sparsi_secondo_livello:
        
        #Per rendere il calcolo più efficiente, aggiorniamo la lista dei retweet fra cui cercare ad ogni iterazione
        retweet_sparsi_secondo_livello = list(retweets_tree.loc[(retweets_tree["retweeted_user_id"].isin(retweet_sparsi_secondo_livello)) & (retweets_tree["original_tweet_id"] == tweet_id)]["retweeter_user_id"])
        retweet_sparsi_secondo_livello = list(set(retweet_sparsi_secondo_livello)) # elimina i doppioni
        
        #Controllo contro i loop
        for item in retweet_sparsi_secondo_livello:
            if item in retweet_sparsi_totali:
                retweet_sparsi_secondo_livello.remove(item)
        
        retweet_sparsi_totali += retweet_sparsi_secondo_livello
        
    return retweet_sparsi_totali

#Preso un insieme di gruppi di utenti (divisi per livelli), calcola quanti retweet hanno preso rispetto al loro livello
#NOTA: users_target si suppone senza il livello sorgente, così come il ritorno
def get_retweet_ratio(users_target_per_level, tweet_id):
    
    tweet_id = int(tweet_id) #Serve per fare le query con pandas
    retweets_tree = pd.read_csv(PATH_FILE_RETWEET_TREE)
    
    next_level = [(get_author(tweet_id))]    
    level_counter = 0    
    ratio_per_level = []
    
    for users_target in users_target_per_level:
        
        #Si saltano l'ultimo livello e quello relativo ai tweet sparsi
        if level_counter >= len(users_target_per_level) - 2:
            break
        
        #Calcoliamo l'insieme degli utenti che appartengono al livello su cui stiamo lavorando
        next_level = list(retweets_tree.loc[(retweets_tree["retweeted_user_id"].isin(next_level)) & (retweets_tree["original_tweet_id"] == tweet_id)]["retweeter_user_id"])
        
        #Calcoliamo il numero di retweet ottenuti da tutti gli utenti di questo livello
        retweet_totali = len(list(retweets_tree.loc[(retweets_tree["retweeted_user_id"].isin(next_level)) & (retweets_tree["original_tweet_id"] == tweet_id)]["retweeter_user_id"]))
        
        #Calcoliamo il numero di retweet ottenuti dagli utenti target di questo livello
        retweet_target = len(list(retweets_tree.loc[(retweets_tree["retweeted_user_id"].isin(users_target)) & (retweets_tree["original_tweet_id"] == tweet_id)]["retweeter_user_id"]))
        
        #Calcoliamo il rapporto
        ratio_per_level.append(retweet_target / retweet_totali)
        
        level_counter += 1
    
    return ratio_per_level
