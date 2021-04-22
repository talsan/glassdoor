import pandas as pd
import os
import json

entity_dir = './google_results/json/'
entity_links = [entity_dir + f for f in os.listdir(entity_dir)]

names = pd.read_csv('./company_queries_2020_12_18.csv')
existing_output = pd.read_csv('./top_google_results_2020_12_18.csv')

output = []
for link in entity_links:
    with open(link, 'r') as f:
        json_data = json.load(f)

    if json_data.get('items') is not None:
        links = [i.get('link', '') for i in json_data.get('items')]
        links_df = pd.DataFrame({'rank': range(1, len(links) + 1), 'link': links})
        output.append(pd.DataFrame({'factset_entity_id': link.rsplit('/')[-1].replace('.json',''),
                                    'result_rank': range(1, len(links) + 1),
                                    'gd_link': links}))
output_df = pd.concat(output)

all_data = names.merge(output_df, how='left', on='factset_entity_id')
all_data.to_csv('./google_results/top_google_results_2020_12_18.csv')
