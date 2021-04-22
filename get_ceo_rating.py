from selenium import webdriver
import pandas as pd
import os
import traceback
import json
import time
from random import randint

link_list = pd.read_csv('./google_results/top_google_results_2020_12_18.csv')
link_list_top = link_list.loc[link_list['result_rank'] == 1, 'gd_link'].to_list()

hard_maps = pd.read_csv('./google_results/hard_maps.csv')['gd_link'].to_list()

link_list_all = link_list_top + hard_maps

# already processed files
overviews = os.listdir('./extracts/overview')
overview_extras = os.listdir('./extracts/overview_extra')
datas = os.listdir('./extracts/data')
errors = os.listdir('./extracts/errors')

# link = 'https://www.glassdoor.com/Overview/Working-at-IBM-EI_IE354.11,14.htm'
# link = 'https://www.glassdoor.com/Overview/Working-at-Microsoft-EI_IE1651.11,20.htm'
# link_cln = link.rsplit('/')[-1]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

for link in link_list_all:

    link_cln = link.rsplit('/')[-1]
    print(link_cln)

    if link_cln not in overviews + errors:

        try:
            driver = webdriver.Chrome(executable_path='./chrome_driver/chromedriver.exe', options=chrome_options)
            driver.get(link)
            raw_html = driver.page_source
            with open(f'./extracts/overview/{link_cln}', 'w', encoding='utf-8') as f:
                f.write(raw_html)

            time.sleep(randint(2, 5))
            link_cln_json = link_cln.replace('htm', 'json')
            ceo_rating = driver.find_element_by_css_selector('#EmpStats_Approve .textVal').text
            company_home_page = driver.find_element_by_css_selector('a[data-test="employer-website"]').text
            with open(f'./extracts/data/{link_cln_json}', 'w') as f:
                json.dump({'ceo_rating': ceo_rating,
                           'homepage': company_home_page}, f)

            driver.find_element_by_css_selector('div[data-test="statsLink"] div .SVGInline').click()
            raw_html_extra = driver.page_source
            with open(f'./extracts/overview_extra/{link_cln}', 'w', encoding='utf-8') as f:
                f.write(raw_html_extra)

        except BaseException as err:
            print(str(err))
            with open(f'./extracts/errors/{link_cln}', 'w') as f:
                f.write(str(err))
                f.write(traceback.format_exc())

        driver.quit()
        time.sleep(randint(10, 30))

    else:
        print('already processed')
