# ADM-HW3

## 1. Data Collection

For readability purpose we used python files with the below functions and purposes.

#### Functions in urlcollector.py

`get_last_page_number() `: Scrapes the first page of the restaurant listings to determine the total number of pages (based on pagination links). It finds the highest page number and returns it.

`scrape_details_restaurant(html_content)`:Extracts restaurant details from the HTML content of a page. It specifically looks for the restaurant link and appends the restaurant URLs to a file (restaurants.txt).


`fetch_and_save(session, page_number)` : Asynchronously fetches the HTML content of a specific page (using the page number), and then passes that content to scrape_details_restaurant for processing.

`scrape_sequentially(last_page)`: Loops through all pages (from 1 to the last page) and sequentially fetches and saves the HTML content of each page using fetch_and_save.


#### Functions in crawler.py

`download_restaurant_html(session, url, folder_name, file_name)`: Asynchronously downloads the HTML content of a single restaurant’s page, saves it to a file in the specified folder, and ensures the folder is created if it doesn't exist.

`download_batch(session, batch_urls, batch_number)`: Downloads a batch of restaurant pages (from the URLs provided), and for each URL in the batch, it creates and saves the HTML content into individual files.

`batch_download_restaurants()`: Reads URLs from restaurants.txt, splits them into batches, and asynchronously downloads each batch using download_batch. It processes all the URLs in batches of 20.

#### Functions in parser.py

`extract_data_from_html(html_content)`: This function processes a single HTML page (offline saved restaurant's detailed page) and extracts specific data such as the restaurant’s name, address, cuisine type, price range, phone number, description, services, website, and payment methods.

This function returns a dictionary containing the extracted details for one restaurant, including restaurantName, address, city, postalCode, country, priceRange, cuisineType, description, facilitiesServices, creditCards, phoneNumber, and website.

`process_saved_pages()`: This function scans through all the saved HTML pages stored in folders (e.g., page1, page2,...pagen), reads each HTML file, extracts restaurant data using the extract_data_from_html() function, and aggregates the results.

This function saves the datafram into `restaurant.tsv` which makes it ready for further preprocessing.

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

## 3. Define a New Score
This section ranks restaurants based on user-provided queries and preferences. It uses a custom scoring algorithm to deliver the results.

### Key Features

- **Query Matching**: Matches the user’s input query with restaurant descriptions for relevance.
- **Custom Scoring**: Considers multiple factors such as cuisine types, facilities, and price ranges to calculate a composite score for each restaurant.
- **Top-K Recommendations**: Returns the top-ranked restaurants based on the computed scores.

### Workflow

1. Users provide a query (e.g., "modern seasonal cuisine") and their preferences, such as cuisine type, facilities, and price range.
2. The system matches restaurants based on query similarity and evaluates them against user preferences.
3. Restaurants are ranked using a custom scoring algorithm that gives weighted importance to each factor.
4. The top results are presented to the user, including relevant details like the restaurant’s name, address, description, and website.

### Output

The system generates a ranked list of restaurants, helping users discover the best options that match their needs.

## 4. Visualizing the Most Relevant Restaurants

This section focuses on mapping Michelin-starred restaurants in Italy while associating additional attributes like price ranges and geographical coordinates.

### Objectives
- Compile a list of unique locations in Italy formatted as `(City, Region)`.
- Retrieve accurate geographical coordinates (latitude and longitude) for these locations using GPT-4.
- Associate price range data with each city by calculating the approximate arithmetic mean of the price ranges of all restaurants in that city.

### Procedures

1. **Required Features**:
   - Extracted a list of unique cities and regions from Michelin restaurant data.
   - Computed the mean price range for each city based on its restaurants' data.

2. **Geographical Coordinates**:
   - Used GPT-4 to obtain accurate coordinates for the `(City, Region)` tuples.
   - Ensured correctness and consistency of the retrieved location data.

3. **Data Preparation**:
   - Consolidated all restaurant attributes, including location, price range, and coordinates, for mapping purposes.

4. **Map Creation**:
   - Installed and utilized the `plotly` library for visualization.
   - Integrated a GeoJSON file outlining the 20 Italian regions.
   - Plotted cities as dots on the map, using color-coding to represent different price range levels.

### Output
The final map provides a visual representation of Michelin-starred restaurants in Italy, displaying:
- Cities marked with dots.
- Price range levels represented through a color gradient.

## 5. BONUS: Advanced Search Engine

1. **Preprocessing**: 
   - The data has been preprocessed to prepare it for transformation into a vector.
   - Cosine similarity was computed based on the restaurant name, city, and cuisine type.

2. **Aggregation and Normalization**:
   - The computed similarity scores were aggregated.
   - These scores were then normalized to a range between 0 and 1 to ensure consistent comparison.

3. **Filtering**:
   - A series of filters were applied to the results:
     - **Price range**
     - **Region**
     - **Accepted credit cards**
     - **Services and facilities** 
   
4. **Final Filtered Results**:
   - The final filtered result set is returned.


## Algorithmic Question (AQ)

Input: Number of test cases `t` and for each test case:
       Number of packages `n` and their coordinates `(x1, y1), (x2, y2), ..., (xn, yn)`
Output: "YES" and the lexicographically smallest path for each test case, or "NO" if impossible

For this section it consists of the pseudocode, prove of the algorithm, 
computes the time complexity, evaluate the time complexity using LLM tool and
lastly prove the greedy algorithm is optimal.
