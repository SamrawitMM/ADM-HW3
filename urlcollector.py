import requests
from bs4 import BeautifulSoup

# Get the last page number based on pagination from the first page
def get_last_page_number():
    url = 'https://guide.michelin.com/en/it/restaurants'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Select all pagination items
    pagination = soup.select(".pagination li a")

    # Extract the text of each pagination link, convert to integer if it’s a number
    page_numbers = [
        int(link.get_text()) for link in pagination if link.get_text().isdigit()
    ]

    # Return the maximum page number found
    return max(page_numbers) if page_numbers else 1  # Fallback to 1 if no pagination found


# Function to extract restaurant details from a single page's HTML content
def scrape_details_restaurant(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all restaurant cards (each restaurant is wrapped in a div with class 'card__menu')
    restaurants = soup.find_all('div', class_='card__menu')

    for restaurant in restaurants:
        # Extract the link (from <a> tag inside 'card__menu-content--title')
        name_tag = restaurant.find('h3', class_='card__menu-content--title')
        link_tag = name_tag.find('a') if name_tag else None
        link = link_tag['href'] if link_tag else 'No link found'

        # Write the link to the 'restaurants.txt' file
        with open("restaurants.txt", 'a', encoding='utf-8') as file:
            file.write('https://guide.michelin.com' + link + "\n")  # Append the link and add a new line


# Asynchronous function to fetch the HTML content for each page (sequentially)
async def fetch_and_save(session, page_number):
    url = f'https://guide.michelin.com/en/it/restaurants/page/{page_number}'
    async with session.get(url) as response:
        if response.status == 200:
            html_content = await response.text()
            scrape_details_restaurant(html_content)  # Scrape the details from the page
        else:
            print(f"Failed to retrieve page {page_number}, status: {response.status}")


# Function to scrape all pages based on the last page number, iterating sequentially
async def scrape_sequentially(last_page):
    import aiohttp
    async with aiohttp.ClientSession() as session:
        for page_number in range(1, last_page + 1):
            print(f"Scraping page {page_number}...")
            await fetch_and_save(session, page_number)  # Scrape each page sequentially
