import csv
import FollowingHandler
import RetweetersHandler

PATH_FILE_METRICS = "../../dataset/Dataset formato CSV/metrics.csv"
PATH_FILE_METRICS_PARZIALI = "../../dataset/Dataset formato CSV/metrics_parziali.csv"

with open(PATH_FILE_METRICS, encoding = "utf8") as file_metrics, open(PATH_FILE_METRICS_PARZIALI, 'w', newline = '') as file_metrics_parziali:
    reader = csv.DictReader(file_metrics)
    writer = csv.writer(file_metrics_parziali)
    
    x = FollowingHandler.FollowingHasher()
    
    for row in reader:
        
        author = RetweetersHandler.get_author(row['original_tweet_id'])
        
        if author == -1:
            continue
        
        if x.get_following(author) != None:
            writer.writerow([str(row['original_tweet_id'])])