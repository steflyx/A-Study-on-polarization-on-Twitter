import csv
import os

#Alcune costanti utili per orientarsi meglio nel lavorare con gli array
PRESENT = 1
ABSENT = 0
USER = 0
FOLLOWING_INDEX = 1
PATH_USER_INDEX_FILE = '../../dataset/Dataset formato CSV/UserIndex.csv'
PATH_FOLLOWING_TABLE_FILE = '../../dataset/Dataset formato CSV/FollowingTable.csv'
PATH_LINK_FILE = '../../dataset/Dataset formato CSV/links.csv'



#Questa classe si occupa di gestire i dati riguardanti le relazioni follower-following
#Il suo funzionamento è il seguente:
# - Il costruttore prende come argomento il nome del file dove è salvata tale relazione
# - Se è la prima volta che viene chiamato, apre il file e smista le informazioni (1)
# - Le informazioni ordinate vengono salvate su due file
# - La volta successiva che il costruttore viene chiamato, vedrà che i file esistono già 
#   e preleverà le informazioni da lì, invece che riordinarle nuovamente
# - Per ottenere i following di un utente dall'esterno, è sufficiente chiamare 'get_following(user)'
#
#(1) Lo smistamento avviene così:
#       - Esistono due array: registered_users e following
#       - Il primo è costituito da coppie [{user}, {indice}]
#                                         user --> id di un utente
#                                         indice --> indice dell'array following dell'utente corrispondente
#       - Il secondo è costituito da liste contenente le informazioni sui following dei vari utenti
#
#
class FollowingHasher:
    
    #Costruttore che inizializza i due array utilizzati per l'archiviazione delle informazioni
    def __init__(self, links_filename=PATH_LINK_FILE):
        
        #Lista di coppie {user, indice} ordinata in maniera crescente secondo 'user'
        #user --> id di un utente
        #indice --> indice dell'array 'following' dove è possibile trovare i following dell'utente corrispondente
        self.registered_users = []
        
        #lista di array contenente i following dei vari utenti; sono ordinati per indice
        self.following = []
        
        #Controlla se la tabella ordinata era già stata costruita precedentemente, nel qual caso la carica, altrimenti la crea e la salva
        if os.path.exists(PATH_USER_INDEX_FILE) and os.path.exists(PATH_FOLLOWING_TABLE_FILE):
            self.load_hash_information()
        else:
            self.hash_following_information(links_filename)
    
    
    
    #Ritorna PRESENT se l'utente è presente, altrimenti ritorna l'indice dove va posizionato
    def is_user_present(self, user):
        
        for i in range(len(self.registered_users)):
            if self.registered_users[i][USER] == user:
                return [PRESENT, self.registered_users[i][FOLLOWING_INDEX]]
            if self.registered_users[i][USER] > user:
                return [ABSENT, i]
        return [ABSENT, len(self.registered_users)]
    
    
    #Aggiunge una coppia user-following. Questa funzione ordina l'array 'registered_users' in 
    #maniera crescente, rendendo lo smistamento dei link piuttosto inefficiente. Utilizzare la
    #funzione successiva per grandi quantità di dati
    def add_link_ordered(self, source, target):
        
        pos = self.is_user_present(source)
        
        #Se l'utente era già presente, aggiungiamo il target alla lista dei suoi following
        if pos[0] == PRESENT:
            self.following[pos[1]].append(target)
        
        #Altrimenti si crea una nuova entry nei due array
        else:
            self.registered_users.insert(pos[1], [source, len(self.following)])
            self.following.append([target])
        
    #Aggiunge una coppia user-following. Per rendere più efficiente questo lavoro, non si
    #ordina 'registered_users' in alcun modo. Semplicemente si controlla se l'utente di cui
    # stiamo salvando il following è lo stesso della precedente iterazione, nel qual caso
    #sappiamo già di doverlo inserire nell'ultima entry di 'following'. Se l'utente dovesse
    #ripresentarsi successivamente, si creerà un'entry duplicata, motivo per cui 'registered_users'
    #andrebbe riaggiustato dopo aver terminato il lavoro    
    def add_link(self, source, target, last_added):
        
        #Se l'ultimo utente inserito è diverso da quello attuale, si crea una nuova entry
        if last_added != source:
            self.registered_users.append([source, len(self.following)])
            self.following.append([target])
            return source
        #Altrimenti, inseriamo l'informazione nell'ultima entry di 'following'
        else:
            self.following[len(self.following)-1].append(target)
            return last_added
        
                
    #Apre il file 'links_filename' e smista i following utilizzando le due funzioni appena definite
    #dopodiché salva le informazioni su due file
    def hash_following_information(self, links_filename):
        
        with open(links_filename, encoding="utf8") as f:
            linkReader = csv.DictReader(f)
            count = perc = 0
            last_added = ''
            
            for row in linkReader:
                
                #Aggiunta del link
                last_added = self.add_link(row['source_id'], row['target_id'], last_added)
                
                #Info sulla percentuale di completamento
                if count % 100 == 0:
                    perc += 0.00011
                    print(perc)
                count += 1
                
        #Prima di salvare le informazioni, 'registered_users' viene salvato
        self.sort_registered_users()
        self.save_hash_information()
            
    #Restituisce un array contenente i following di un utente
    def get_following(self, user):
        
        user_position = self.find_user_position(self.registered_users, 0, len(self.registered_users)-1, user)        

        return self.following[int(self.registered_users[user_position][FOLLOWING_INDEX])] if user_position != -1 else None


    #Implementa una ricerca binaria per trovare l'id di un utente
    def find_user_position(self, array, inf, sup, user_id):
        
        if inf > sup or sup < inf or array[inf][USER] > user_id or array[sup][USER] < user_id:
            return -1
        
        mid = (inf + sup)//2
        if array[mid][USER] == user_id:
            return mid
        
        return self.find_user_position(array, inf, mid-1, user_id) if array[mid][USER] > user_id else self.find_user_position(array, mid+1, sup, user_id)
    
    #Salva registered_users e following in due file 'UserIndex.csv' e 'FollowingTable.csv'
    def save_hash_information(self):
        
        print('Salvando i file...')
        
        with open(PATH_USER_INDEX_FILE, 'w', newline='') as User_Index_File, open(PATH_FOLLOWING_TABLE_FILE, 'w', newline='') as Following_Table_File:
            writer_user_index = csv.writer(User_Index_File)
            writer_following_table = csv.writer(Following_Table_File)  
            writer_user_index.writerows(self.registered_users)
            print('UserIndex.csv salvato')
            writer_following_table.writerows(self.following)
            print('FollowingTable.csv salvato')
            
    
    #Legge dai file 'UserIndex.csv' e 'FollowingTable.csv' i valori di registered_users e following_table
    def load_hash_information(self):
        
        print('Caricando i file...')
        
        with open(PATH_USER_INDEX_FILE, encoding="utf8") as User_Index_File, open(PATH_FOLLOWING_TABLE_FILE, encoding="utf8") as Following_Table_File:
            reader_user_index = csv.reader(User_Index_File)
            reader_following_table = csv.reader(Following_Table_File)  
        
            #Info sull'indicizzazione dei following
            self.registered_users = []
            for row in reader_user_index:
                self.registered_users.append(row)
                
            #Following ordinati
            self.following = []
            for row in reader_following_table:
                self.following.append(row)
                
        print('File caricati')
    
    
    #Check dei risultati
    def check_results(self):
        
        following = []
        
        with open(PATH_LINK_FILE, encoding="utf8") as f:
            linkReader = csv.DictReader(f)
            count = perc =0
            
            for row in linkReader:
                
                if row['source_id'] == '887035878':
                    following.append(row['target_id'])
                    
                #Info sulla percentuale di completamento
                if count % 100 == 0:
                    perc += 0.00011
                    print(perc)
                count += 1
                    
        if self.check_if_equals(following, self.get_following('887035878')):
            print("Ok")
        else:
            print("Non ok")
        
    #Ordina 'registered_users' in maniera crescente, così da rendere più efficienti gli accessi futuri
    #Inoltre si occupa di eliminare eventuali doppioni
    def sort_registered_users(self):

        #Si ordina l'array
        self.registered_users = sorted(self.registered_users)
        
        #Si controllano gli elementi adiacenti per controllare se hanno stesso user_id
        for i in range(0, len(self.registered_users)-2):
            
            while self.registered_users[i][USER] == self.registered_users[i+1][USER]:
                
                self.following[self.registered_users[i][FOLLOWING_INDEX]] += self.registered_users[i+1][FOLLOWING_INDEX]
                self.registered_users.remove(self.registered_users[i+1])
                if i == len(self.registered_users)-1:
                    break
        
    def check_if_equals(self, array1, array2):
        for i in array1:
            if i not in array2:
                print(i + " non in get_following")
                return False
        return True
    