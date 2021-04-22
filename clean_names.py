import pandas as pd
import re
from collections import Counter

names = pd.read_csv('all_2020_12_18.csv')[['factset_entity_id','proper_name']].drop_duplicates()
all_names = ' '.join(names['proper_name']).lower()
all_names = re.sub('[^a-z]', ' ', all_names)
all_names = re.sub('\\b.{1}\\b', ' ', all_names)
all_names = re.sub('\\s+', ' ', all_names)

name_count = Counter(all_names.split(' ')).most_common(100)
stop_names_count = [(k, v) for k, v in name_count]
stop_names_raw = [k for k, v in name_count]

stop_names = ['inc', 'class', 'ltd', 'corporation', 'co', 'limited', 'corp', 'company',
              'plc', 'sa', 'of', 'sab','nav','com','pt','tbk','ad','se','nv',
              'ag', 'trust', 'incorporated', 'de',
              'sponsored', 'services', 'adr', 'nvdr',
              'bhd', 'ab', 'series','warrant','holding','rt','pfd','non','voting','an']

def clean_names(name):
    name = name.lower()
    name = re.sub('[^a-z0-9]', ' ', name)
    name = re.sub('\\b.{1}\\b', ' ', name)
    name = re.sub('\\b\\d*\\b', ' ', name)
    name = re.sub('\\s+', ' ', name)
    name = ' '.join([n for n in name.split(' ') if n not in stop_names])
    return name.strip()

names['search_query'] = names['proper_name'].apply(clean_names)
names.to_csv('./company_queries_2020_12_18.csv',index=False)