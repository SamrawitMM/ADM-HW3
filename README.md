# ADM-HW3

## 1. Data Collection
We used **Beautiful Soup** to scrape data from a webpage. The process involved iterating through the pagination and storing the URLs in `restaurant.txt`. Then, we downloaded the HTML of each restaurant page from the stored URLs and proceeded to scrape the following information:

- Restaurant name
- Address
- City
- Postal code
- Country
- Price range
- Cuisine type
- Description
- Facilities and services
- Accepted credit cards
- Phone number
- URL to the restaurant page

Once the information was scraped offline, we saved the data into `restaurant.tsv` for further processing.

## 2. Search Engine
For the search engine, we preprocessed the **description** column of the dataset. The preprocessing steps included:
- Removing **stopwords**
- Removing **punctuation**
- Applying **stemming** to reduce words to their base form.

Next, we assigned a `term_id` to each unique word and built **inverted indexes** by pairing each `term_id` with a list of document IDs where the term appears. 

When a query is provided, the system searches the **description** column of the dataset and returns a list of restaurants with the following features:
- Restaurant name
- Address
- Description
- Website URL

To rank the search results, we calculated the **Term Frequency (TF)** and **Inverse Document Frequency (IDF)** for both the restaurant descriptions and the search query. The **cosine similarity** was then calculated based on these scores, and the results were displayed according to their similarity score.

## 3. 
