import requests
import pandas as pd

company_query = 'ibm'

url = 'https://www.googleapis.com/customsearch/v1/siterestrict?'
cx = 'fc57dcaee3e766655'
key = 'AIzaSyDL17XgQVZ2n7TfZG_S7CrZax14x1w-ilM'

names = pd.read_csv('./company_queries_2020_12_18.csv')
existing_output = pd.read_csv('./top_google_results_2020_12_18.csv')

output = []
for i, r in names.iterrows():
    print(r)
    if r['factset_entity_id'] not in existing_output['factset_entity_id'].to_list():
        query_string = {"key": key, "cx": cx, "q": r['search_query']}
        response = requests.get(url, params=query_string)
        json_data = response.json()
        if json_data.get('items') is not None:
            links = [i.get('link','') for i in json_data.get('items')]
            links_df = pd.DataFrame({'rank': range(1, len(links) + 1), 'link': links})
            output.append(pd.DataFrame({'factset_entity_id': r['factset_entity_id'],
                                        'proper_name':r['proper_name'],
                                        'search_query':r['search_query'],
                                        'result_rank': range(1, len(links) + 1),
                                        'gd_link': links}))
        else:
            print('*** no results available for ***')
            print(r)
    else:
        print('*** already processed for ***')
        print(r)

output_df = pd.concat(output)
output_full = pd.concat([existing_output,output_df])

output_full.to_csv('./google_results/top_google_results_2020_12_18.csv',index=False)