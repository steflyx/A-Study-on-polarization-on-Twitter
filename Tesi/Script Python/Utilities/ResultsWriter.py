import csv
import pandas as pd
from shutil import copyfile

PATH_FILE_METRICS = "../../dataset/Dataset formato CSV/metrics.csv"
PATH_FILE_RESULTS_JACCARD_NODE = "../../Risultati/Jaccard_Node/Jaccard_Node_Results.csv"
PATH_FILE_RESULTS_LINEAR_FIT = "../../Risultati/Linear_Fit/Linear_Fit_Results.csv"
PATH_FILE_RESULTS_PERCENTILI = "../../Risultati/Percentili/Percentili_Results_Per_Cascade.csv"
PATH_FILE_RESULTS_INFLUENCE = "../../Risultati/Influence/Influence_Results.csv"
PATH_FILE_RESULTS_LEVEL = "../../Risultati/Jaccard_Level/Jaccard_Level_Results.csv"
PATH_FILE_RESULTS_PERCENTILI_LEVEL = "../../Risultati/Percentili/Percentili_Results_Per_Level.csv"

PATH_FILE_FINAL_RESULTS = "../../Risultati/Finali/Node_Results.csv"
PATH_FILE_FINAL_LEVEL_RESULTS = "../../Risultati/Finali/Level_Results.csv"
PATH_FILE_FINAL_PERCENTILI_LEVEL_RESULTS = "../../Risultati/Finali/Percentili_Per_Level_Results.csv"

FIELDNAMES_RESULTS = ['original_tweet_id', 'n_retweets', 'depth', 'tree_ratio', 'disc_perc', 'first_perc', 'root_msg_strength', 'node_msg_strength_mean', 'node_msg_strength_mode', 'node_msg_strength_median', 'node_msg_strength_std', 'node_msg_strength_skw', 'node_msg_strength_kur', 'lvl_msg_strength_mean', 'lvl_msg_strength_mode', 'lvl_msg_strength_median', 'lvl_msg_strength_std', 'lvl_msg_strength_skw', 'lvl_msg_strength_kur', 'lvl_retweets_strength_mean', 'lvl_retweets_strength_mode', 'lvl_retweets_strength_median', 'lvl_retweets_strength_std', 'lvl_retweets_strength_skw', 'lvl_retweets_strength_kur', 'max_lvl_retweets', 'lvl_retweets_gt_first', 'lvl_perc_retweeted_mean', 'lvl_perc_retweeted_mode', 'lvl_perc_retweeted_median', 'lvl_perc_retweeted_std', 'lvl_perc_retweeted_skw', 'lvl_perc_retweeted_kur', 'usr_diff_mean', 'usr_diff_mode', 'usr_diff_median', 'usr_diff_std', 'usr_diff_skw', 'usr_diff_kur', 'lvl_usr_diff_mean', 'lvl_usr_diff_mode', 'lvl_usr_diff_median', 'lvl_usr_diff_std', 'lvl_usr_diff_skw', 'lvl_usr_diff_kur', 'lvl_usr_diff_slope', 'lvl_usr_diff_gof', 'lvl_usr_diff_intercept', '25_outlier_retweet_perc_mean', '25_outlier_retweet_perc_mode', '25_outlier_retweet_perc_median', '25_outlier_retweet_perc_std', '25_outlier_retweet_perc_skw', '25_outlier_retweet_perc_kur', '25_outlier_retweet_perc_max', '5_outlier_retweet_perc_mean', '5_outlier_retweet_perc_mode', '5_outlier_retweet_perc_median', '5_outlier_retweet_perc_std', '5_outlier_retweet_perc_skw', '5_outlier_retweet_perc_kur', '5_outlier_retweet_perc_max', '25_max_lvl', '5_max_lvl', 'influencer_mean', 'influencer_mode', 'influencer_median', 'influencer_std', 'influencer_skw', 'influencer_kur']

#Copiamo i file con i risultati per livello
copyfile(PATH_FILE_RESULTS_LEVEL, PATH_FILE_FINAL_LEVEL_RESULTS)
copyfile(PATH_FILE_RESULTS_PERCENTILI_LEVEL, PATH_FILE_FINAL_PERCENTILI_LEVEL_RESULTS)

#Apriamo i file con i risultati per nodo
jaccard_node_results = pd.read_csv(PATH_FILE_RESULTS_JACCARD_NODE)
linear_fit_results = pd.read_csv(PATH_FILE_RESULTS_LINEAR_FIT)
percentili_results = pd.read_csv(PATH_FILE_RESULTS_PERCENTILI)
influence_results = pd.read_csv(PATH_FILE_RESULTS_INFLUENCE)

#Riportiamo i risultati per nodo nel file finale
with open(PATH_FILE_METRICS, encoding = "utf8") as file_metrics, open(PATH_FILE_FINAL_RESULTS, 'w', newline = '') as file_results:
    
    reader_metrics = csv.DictReader(file_metrics)
    writer_results = csv.DictWriter(file_results, fieldnames = FIELDNAMES_RESULTS)
    writer_results.writeheader()
    
    updated_metrics = []
    
    for row in reader_metrics:

        #Recuperiamo i risultati per nodo
        #Indici interessati: 'usr_diff_mean', 'usr_diff_mode', 'usr_diff_median', 'usr_diff_std', 'usr_diff_skw', 'usr_diff_kur'
        jaccard_node_row = jaccard_node_results.loc[jaccard_node_results['original_tweet_id'] == int(row['original_tweet_id'])]
        if jaccard_node_row.empty:
            jaccard_node_row_results = {'usr_diff_mean': 'NULL', 'usr_diff_mode': 'NULL', 'usr_diff_median': 'NULL', 'usr_diff_std': 'NULL', 'usr_diff_skw': 'NULL', 'usr_diff_kur': 'NULL'}
        else:
            jaccard_node_row_results = {'usr_diff_mean': float(jaccard_node_row['usr_diff_mean']), 'usr_diff_mode': float(jaccard_node_row['usr_diff_mode']), 'usr_diff_median': float(jaccard_node_row['usr_diff_median']), 'usr_diff_std': float(jaccard_node_row['usr_diff_std']), 'usr_diff_skw': float(jaccard_node_row['usr_diff_skw']), 'usr_diff_kur': float(jaccard_node_row['usr_diff_kur'])}
        
        
        #Recuperiamo i risultati del fit lineare
        #Indici interessati: 'lvl_usr_diff_slope', 'lvl_usr_diff_gof', 'lvl_usr_diff_intercept'
        linear_fit_row = linear_fit_results.loc[linear_fit_results['original_tweet_id'] == int(row['original_tweet_id'])]
        if linear_fit_row.empty:
            linear_fit_row_results = {'lvl_usr_diff_slope': 'NULL', 'lvl_usr_diff_gof': 'NULL', 'lvl_usr_diff_intercept': 'NULL'}
        else:
            linear_fit_row_results = {'lvl_usr_diff_slope': float(linear_fit_row['lvl_usr_diff_slope']), 'lvl_usr_diff_gof': float(linear_fit_row['lvl_usr_diff_gof']), 'lvl_usr_diff_intercept': float(linear_fit_row['lvl_usr_diff_intercept'])}
        
        
        #Recuperiamo i risultati dei percentili
        #Indici interessati: '25_outlier_retweet_perc_mean', '25_outlier_retweet_perc_mode', '25_outlier_retweet_perc_median', '25_outlier_retweet_perc_std', '25_outlier_retweet_perc_skw', '25_outlier_retweet_perc_kur', '25_outlier_retweet_perc_max', '5_outlier_retweet_perc_mean', '5_outlier_retweet_perc_mode', '5_outlier_retweet_perc_median', '5_outlier_retweet_perc_std', '5_outlier_retweet_perc_skw', '5_outlier_retweet_perc_kur', '5_outlier_retweet_perc_max', '25_max_lvl', '5_max_lvl'
        percentili_row = percentili_results.loc[percentili_results['original_tweet_id'] == int(row['original_tweet_id'])]
        if percentili_row.empty:
            percentili_row_results = {'25_outlier_retweet_perc_mean': 'NULL', '25_outlier_retweet_perc_mode': 'NULL', '25_outlier_retweet_perc_median': 'NULL', '25_outlier_retweet_perc_std': 'NULL', '25_outlier_retweet_perc_skw': 'NULL', '25_outlier_retweet_perc_kur': 'NULL', '25_outlier_retweet_perc_max': 'NULL', '5_outlier_retweet_perc_mean': 'NULL', '5_outlier_retweet_perc_mode': 'NULL', '5_outlier_retweet_perc_median': 'NULL', '5_outlier_retweet_perc_std': 'NULL', '5_outlier_retweet_perc_skw': 'NULL', '5_outlier_retweet_perc_kur': 'NULL', '5_outlier_retweet_perc_max': 'NULL', '25_max_lvl': 'NULL', '5_max_lvl': 'NULL'}
        else:
            percentili_row_results = {'25_outlier_retweet_perc_mean': float(percentili_row['25_outlier_retweet_perc_mean']), '25_outlier_retweet_perc_mode': float(percentili_row['25_outlier_retweet_perc_mode']), '25_outlier_retweet_perc_median': float(percentili_row['25_outlier_retweet_perc_median']), '25_outlier_retweet_perc_std': float(percentili_row['25_outlier_retweet_perc_std']), '25_outlier_retweet_perc_skw': float(percentili_row['25_outlier_retweet_perc_skw']), '25_outlier_retweet_perc_kur': float(percentili_row['25_outlier_retweet_perc_kur']), '25_outlier_retweet_perc_max': float(percentili_row['25_outlier_retweet_perc_max']), '5_outlier_retweet_perc_mean': float(percentili_row['5_outlier_retweet_perc_mean']), '5_outlier_retweet_perc_mode': float(percentili_row['5_outlier_retweet_perc_mode']), '5_outlier_retweet_perc_median': float(percentili_row['5_outlier_retweet_perc_median']), '5_outlier_retweet_perc_std': float(percentili_row['5_outlier_retweet_perc_std']), '5_outlier_retweet_perc_skw': float(percentili_row['5_outlier_retweet_perc_skw']), '5_outlier_retweet_perc_kur': float(percentili_row['5_outlier_retweet_perc_kur']), '5_outlier_retweet_perc_max': float(percentili_row['5_outlier_retweet_perc_max']), '25_max_lvl': float(percentili_row['25_max_lvl']), '5_max_lvl': float(percentili_row['5_max_lvl'])}
        
        
        #Recuperiamo i risultati sugli influencer
        #Indici interessati: 'influencer_mean', 'influencer_mode', 'influencer_median', 'influencer_std', 'influencer_skw', 'influencer_kur'
        influence_row = influence_results.loc[influence_results['original_tweet_id'] == int(row['original_tweet_id'])]
        if influence_row.empty:
            influence_row_results = {'influencer_mean': 'NULL', 'influencer_mode': 'NULL', 'influencer_median': 'NULL', 'influencer_std': 'NULL', 'influencer_skw': 'NULL', 'influencer_kur': 'NULL'}
        else:
            influence_row_results = {'influencer_mean': float(influence_row['influencer_mean']), 'influencer_mode': float(influence_row['influencer_mode']), 'influencer_median': float(influence_row['influencer_median']), 'influencer_std': float(influence_row['influencer_std']), 'influencer_skw': float(influence_row['influencer_skw']), 'influencer_kur': float(influence_row['influencer_kur'])}
        
        #Riportiamo tutto nel file finale
        updated_row = {'original_tweet_id': row['original_tweet_id'], 'n_retweets': row['n_retweets'], 'depth': row['depth'], 'tree_ratio': row['tree_ratio'], 'disc_perc': row['disc_perc'], 'first_perc': row['first_perc'], 'root_msg_strength': row['root_msg_strength'], 'node_msg_strength_mean': row['node_msg_strength_mean'], 'node_msg_strength_mode': row['node_msg_strength_mode'], 'node_msg_strength_median': row['node_msg_strength_median'], 'node_msg_strength_std': row['node_msg_strength_std'], 'node_msg_strength_skw': row['node_msg_strength_skw'], 'node_msg_strength_kur': row['node_msg_strength_kur'], 'lvl_msg_strength_mean': row['lvl_msg_strength_mean'], 'lvl_msg_strength_mode': row['lvl_msg_strength_mode'], 'lvl_msg_strength_median': row['lvl_msg_strength_median'], 'lvl_msg_strength_std': row['lvl_msg_strength_std'], 'lvl_msg_strength_skw': row['lvl_msg_strength_skw'], 'lvl_msg_strength_kur': row['lvl_msg_strength_kur'], 'lvl_retweets_strength_mean': row['lvl_retweets_strength_mean'], 'lvl_retweets_strength_mode': row['lvl_retweets_strength_mode'], 'lvl_retweets_strength_median': row['lvl_retweets_strength_median'], 'lvl_retweets_strength_std': row['lvl_retweets_strength_std'], 'lvl_retweets_strength_skw': row['lvl_retweets_strength_skw'], 'lvl_retweets_strength_kur': row['lvl_retweets_strength_kur'], 'max_lvl_retweets': row['max_lvl_retweets'], 'lvl_retweets_gt_first': row['lvl_retweets_gt_first'], 'lvl_perc_retweeted_mean': row['lvl_perc_retweeted_mean'], 'lvl_perc_retweeted_mode': row['lvl_perc_retweeted_mode'], 'lvl_perc_retweeted_median': row['lvl_perc_retweeted_median'], 'lvl_perc_retweeted_std': row['lvl_perc_retweeted_std'], 'lvl_perc_retweeted_skw': row['lvl_perc_retweeted_skw'], 'lvl_perc_retweeted_kur': row['lvl_perc_retweeted_kur'], 'usr_diff_mean': jaccard_node_row_results['usr_diff_mean'], 'usr_diff_mode': jaccard_node_row_results['usr_diff_mode'], 'usr_diff_median': jaccard_node_row_results['usr_diff_median'], 'usr_diff_std': jaccard_node_row_results['usr_diff_std'], 'usr_diff_skw': jaccard_node_row_results['usr_diff_skw'], 'usr_diff_kur': jaccard_node_row_results['usr_diff_kur'], 'lvl_usr_diff_mean': 'NULL', 'lvl_usr_diff_mode': 'NULL', 'lvl_usr_diff_median': 'NULL', 'lvl_usr_diff_std': 'NULL', 'lvl_usr_diff_skw': 'NULL', 'lvl_usr_diff_kur': 'NULL', 'lvl_usr_diff_slope': linear_fit_row_results['lvl_usr_diff_slope'], 'lvl_usr_diff_gof': linear_fit_row_results['lvl_usr_diff_gof'], 'lvl_usr_diff_intercept': linear_fit_row_results['lvl_usr_diff_intercept'], '25_outlier_retweet_perc_mean': percentili_row_results['25_outlier_retweet_perc_mean'], '25_outlier_retweet_perc_mode': percentili_row_results['25_outlier_retweet_perc_mode'], '25_outlier_retweet_perc_median': percentili_row_results['25_outlier_retweet_perc_median'], '25_outlier_retweet_perc_std': percentili_row_results['25_outlier_retweet_perc_std'], '25_outlier_retweet_perc_skw': percentili_row_results['25_outlier_retweet_perc_skw'], '25_outlier_retweet_perc_kur': percentili_row_results['25_outlier_retweet_perc_kur'], '25_outlier_retweet_perc_max': percentili_row_results['25_outlier_retweet_perc_max'], '5_outlier_retweet_perc_mean': percentili_row_results['5_outlier_retweet_perc_mean'], '5_outlier_retweet_perc_mode': percentili_row_results['5_outlier_retweet_perc_mode'], '5_outlier_retweet_perc_median': percentili_row_results['5_outlier_retweet_perc_median'], '5_outlier_retweet_perc_std': percentili_row_results['5_outlier_retweet_perc_std'], '5_outlier_retweet_perc_skw': percentili_row_results['5_outlier_retweet_perc_skw'], '5_outlier_retweet_perc_kur': percentili_row_results['5_outlier_retweet_perc_kur'], '5_outlier_retweet_perc_max': percentili_row_results['5_outlier_retweet_perc_max'], '25_max_lvl': percentili_row_results['25_max_lvl'], '5_max_lvl': percentili_row_results['5_max_lvl'], 'influencer_mean': influence_row_results['influencer_mean'], 'influencer_mode': influence_row_results['influencer_mode'], 'influencer_median': influence_row_results['influencer_median'], 'influencer_std': influence_row_results['influencer_std'], 'influencer_skw': influence_row_results['influencer_skw'], 'influencer_kur': influence_row_results['influencer_kur']}
        writer_results.writerow(updated_row)