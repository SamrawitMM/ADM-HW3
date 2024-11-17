import aiohttp
import asyncio
import os

# Function to download the HTML content of a single restaurant
async def download_restaurant_html(session, url, folder_name, file_name):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                # Create the folder if it doesn't exist
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                # Save the HTML content to a file 
                with open(os.path.join(folder_name, file_name), 'w', encoding='utf-8') as file:
                    file.write(await response.text())
                    print(f"Downloaded: {file_name} to {folder_name}")
            else:
                print(f"Failed to download {url}, status code: {response.status}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Function to download a batch of URLs
async def download_batch(session, batch_urls, batch_number):
    folder_name = f"page{batch_number}"
    tasks = []

    # Loop through each URL in the batch
    for url in batch_urls:
        # Determine the file name (just the restaurant name, e.g., restaurantname.html)
        restaurant_name = url.split("/")[-1]  # Last part of the URL
        file_name = f"{restaurant_name}.html"  # Save as HTML file

        # Create a task for downloading each URL
        tasks.append(download_restaurant_html(session, url, folder_name, file_name))

    # Wait for all tasks in this batch to complete
    await asyncio.gather(*tasks)

# Function to read URLs from 'restaurants.txt' and batch download them
async def batch_download_restaurants():
    # Read the URLs from 'restaurants.txt'
    with open("restaurants.txt", 'r', encoding='utf-8') as file:
        urls = file.readlines()

    # Strip newline characters from each URL
    urls = [url.strip() for url in urls]

    # Calculate the number of URLs per page (assuming the URL list is evenly distributed)
    total_urls = len(urls)
    urls_per_page = 20  # 20 URLs per folder

    # Create a new session for downloading
    async with aiohttp.ClientSession() as session:
        batch_number = 1

        # Iterate over the URLs in batches of 20
        for i in range(0, total_urls, urls_per_page):
            batch_urls = urls[i:i + urls_per_page]  # Slice the list to get the URLs for this batch
            print(f"Downloading batch {batch_number}...")
            try:
                await download_batch(session, batch_urls, batch_number)
            except Exception as e:
                print(f"Error in batch {batch_number}: {e}")

            batch_number += 1
