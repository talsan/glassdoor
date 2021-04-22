from bs4 import BeautifulSoup
import re
import os
import multiprocessing as mp
import pandas as pd


def extract_from(url):
    print(url)

    output = {'url': url}
    soup = BeautifulSoup(open(f'./extracts/overview/{url}','rb'), 'html.parser',from_encoding='utf-8')

    employer_name = ''
    h1s = soup.select('.tightAll')
    for h1 in h1s:
        if h1.has_attr('data-company'):
            employer_name = h1['data-company']
            continue

    employer_id = soup.find(id='EmpHero')
    employer_id = employer_id['data-employer-id'] if employer_id is not None else ''

    website = soup.find(attrs={'data-test': 'employer-website'})
    website = website.get_text(strip=True) if website is not None else ''

    num_reviews = ''
    info_tbl = soup.find(class_='empLinks tbl')
    if info_tbl is not None:
        reviews_text = info_tbl.find(attrs={'data-label': 'Reviews'})
        if reviews_text is not None:
            reviews_text = reviews_text.get_text(strip=True).lower().replace('reviews','')
            num_reviews_k = ''.join(re.findall('^(\\d*\\.?\\d?k?)', reviews_text))
            if 'k' in num_reviews_k:
                try:
                    num_reviews = str(float(reviews_text.replace('k','')) * 1000)
                except BaseException:
                    print(num_reviews_k)
                    num_reviews = num_reviews_k
            else:
                num_reviews = num_reviews_k

    ceo_name, ceo_num_reviews = '', ''
    ceo_name_reviews = soup.find(class_='ceoName')
    if ceo_name_reviews is not None:
        ceo_name_reviews = ceo_name_reviews.get_text(strip=True, separator='|').split('|')
        ceo_name = ceo_name_reviews[0]
        ceo_num_reviews_text = ceo_name_reviews[1].replace(',','')
        ceo_num_reviews = ''.join(re.findall('^(\\d*)', ceo_num_reviews_text))

    ceo_rating = soup.find(id="EmpStats_Approve")
    ceo_rating = ceo_rating['data-percentage'] if ceo_rating is not None else ''
    ceo_recommend = soup.find(id="EmpStats_Recommend")
    ceo_recommend = ceo_recommend['data-percentage'] if ceo_recommend is not None else ''

    output.update({'employer_id': employer_id,
                   'employer_name': employer_name,
                   'website': website,
                   'num_reviews': num_reviews,
                   'ceo_name': ceo_name,
                   'recommend': ceo_recommend,
                   'ceo_rating': ceo_rating,
                   'ceo_num_reviews': ceo_num_reviews
                   })

    if url in os.listdir('./extracts/overview_extra/'):
        soup_extra = BeautifulSoup(open(f'./extracts/overview_extra/{url}','rb'), "html.parser",from_encoding='utf-8')

        po_text = soup_extra.find(attrs={'data-accordion-category': 'bizOutlook'})
        if po_text is not None:
            po_text = po_text.get_text()
            po_num = ''.join(re.findall('^(\\d\\d?\\d?)', po_text))
        else:
            po_num = ''

        output.update({'positive_outlook': po_num})

        data_cat = ['overallRating', 'cultureAndValues', 'diversityAndInclusion',
                    'workLife', 'seniorManagement', 'compAndBenefits', 'careerOpportunities']

        for dc in data_cat:
            dc_text = soup_extra.find('div', attrs={'data-category': dc})
            if dc_text is not None:
                dc_text = dc_text.get_text()
                dc_num = ''.join(re.findall('(\\d\\.\\d)?$', dc_text))
            else:
                dc_num = ''
            output.update({dc: dc_num})

    return output

if __name__ == '__main__':

    urls = os.listdir('./extracts/overview/')
    urls_extra = os.listdir('./extracts/overview_extra/')

    pool = mp.Pool(processes=mp.cpu_count())
    results = pool.map(extract_from, urls)

    output_df = pd.DataFrame(results)

    output_df.to_csv('extracted_glassdoor.csv',index=False)
