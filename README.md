# Scrape Glassdoor.com

#### 1. Create Google Queries from List of Company Names `clean_names.py`. 
Removes common junk and other share class stuff from name.
Input:  `"all_2020_12_18.csv"`. These is just a list of names we want to collect information on
Output: `company_queries_2020_12_18.csv`

#### 2. Find Top 10 Glassdoor Pages via Google API `get_glassdoor_page.py`
Input: `company_queries_2020_12_18.csv`
Output: `./google_results/json/<company_id>.json`

#### 3. Unpack Google Results `unpack_google_searches.py`
Input: `./google_results/json/<company_id>.json`
Output: `./google_results/top_google_results_2020_12_18.csv`

#### 4. Download HTMLs for Top Results `get_ceo_rating.py`
Input: `./google_results/top_google_results_2020_12_18.csv`
Outputs: 
* `./extracts/overview/<glassdor_link>` (main page)
* `./extracts/overview_extra/<glassdor_link>` (additional info)

#### 5. Download HTMLs for Top Results `get_ceo_rating.py`
Input: `./google_results/top_google_results_2020_12_18.csv`
Outputs: 
* `./extracts/overview/<glassdor_link.html>` (main page)
* `./extracts/overview_extra/<glassdor_link.html>` (additional info)
* `./extracts/errors/<glassdor_link.html>` (pages that encountered errors)
Note: Sleeps randomly (min 10 seconds, max 30 seconds)

#### 5. Extract Structured Data from HTML `extract_from_html.py`
Input: 
* `./extracts/overview/<glassdor_link.html>` (main page)
* `./extracts/overview_extra/<glassdor_link.html>` (additional info)
Outputs: 
* `./extracted_glassdoor.csv`
Note: Uses `multiprocessing` to loop through all the raw html files

#### 6. Build Final Output `build_final_output.py`
Formatting for output specifications; 
Uses company websites from original data to verify mapping with company homepage data item from glassdoor
Input: 
* `./extracted_glassdoor.csv`
Outputs: 
* `./glassdoor_ratings.csv` (main page)
