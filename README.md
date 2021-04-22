# Scrape Ratings from Glassdoor.com
A prototype for scraping glassdoor ratings for a given portfolio holdings file (powered by google's custom search API and Selenium)

### Process Overview
 1. take a list of names from a holdings file 
 2. determine the glassdoor homepage (via google's search api) for each company (using the "cleaned up" company name as the query)
 3. scrape glassdoor's main page for company information and top-level ratings and an additional modal/pop-up for granular ratings (mimicking user clicks via Selenium) 
 4. Organize and merge the output back as columns into the original holdings file.

*This is a prototype for further development. While you might find snippets contained here helpful, 
there is still some hand-holding to get from one step to another, in addition to setting up a google custom search
engine API account, VPN set-up, etc. Feel free to message me if you need any guidance.*  

### Process Details
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
* 
Note: Uses `multiprocessing` to loop through all the raw html files

#### 6. Build Final Output `build_final_output.py`
Formatting for output specifications; 
Uses company websites from original data to verify mapping with company homepage data item from glassdoor
Input: 
* `./extracted_glassdoor.csv`
Outputs: 
* `./glassdoor_ratings.csv` (main page)
