import pandas as pd
import json
from urllib.parse import urljoin
import json
import os
from bs4 import BeautifulSoup


# Function to extract data from a single HTML file and create a DataFrame
def extract_data_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize variables
    address_text = ''
    cuisine = ''
    price_range = ''

    try:
        # Extract address and cuisine information
        address_divs = soup.find_all('div', class_='data-sheet__block--text')

        if len(address_divs) > 0:
            address_text = address_divs[0].get_text(strip=True)  # Extract address text

        if len(address_divs) > 1:
            # Extract cuisine and price information
            cuisine_price_text = address_divs[1].get_text(strip=True)

            # Split cuisine and price by '·' and extract parts
            parts = cuisine_price_text.split('·')

            # Extract price (e.g., € symbols) from the first part
            price_text = parts[0].strip()
            euro_count = price_text.count('€')
            if euro_count > 0:
                price_range = '€' * euro_count

            # Extract cuisine from the second part if it exists
            if len(parts) > 1:
                cuisine = parts[1].strip()

    except IndexError:
        print("Error: Missing expected divs in the HTML content.")
        address_text = ''
        cuisine = ''
        price_range = ''

    # Process the address (split into parts)
    address_parts = address_text.split(',')
    address = address_parts[0].strip() if len(address_parts) > 0 else ''
    city = address_parts[1].strip() if len(address_parts) > 1 else ''
    postal_code = str(address_parts[2].strip()) if len(address_parts) > 2 else ''  # Explicitly cast to string
    country = address_parts[3].strip() if len(address_parts) > 3 else ''

    # print( type(postal_code))
    # print(country)
    # Extract description
    description_div = soup.find('div', class_='data-sheet__description')
    description_text = description_div.get_text(strip=True) if description_div else "Description not available"

    # Extract facilities and services
    services_list = []
    services_div = soup.find('div', class_='restaurant-details__services')
    if services_div:
        service_items = services_div.find_all('li')
        services_list = [item.get_text(strip=True) for item in service_items]

    # Extract phone number
    phone_number_span = soup.find('span', class_='flex-fill')
    phone_number = phone_number_span.get_text(strip=True) if phone_number_span else "Phone number not found"

    # Extract website URL with error handling
    website_link = ''  # Default value
    website_link_tag = soup.find('div', class_='collapse__block-item link-item')

    if website_link_tag:
        # Find the <a> tag inside the div
        a_tag = website_link_tag.find('a', class_='link js-dtm-link')
        if a_tag and a_tag.has_attr('href'):
            website_link = a_tag['href']
            # If the link is relative, make it absolute
            if not website_link.startswith("http"):
                website_link = urljoin('', website_link)

    # print(website_link)


    # Extract JSON data for structured info
    script_tag = soup.find('script', {'type': 'application/ld+json'})
    json_data = {}
    if script_tag:
        try:
            json_data = json.loads(script_tag.get_text(strip=True))
        except json.JSONDecodeError:
            print("Error decoding JSON from the script tag.")

    # Extract information from the JSON if available
    restaurant_name = json_data.get('name', '')
    address = json_data.get('address', {}).get('streetAddress', address)
    city = json_data.get('address', {}).get('addressLocality', city)
    postal_code = json_data.get('address', {}).get('postalCode', postal_code)
    country = json_data.get('address', {}).get('addressCountry', country)
    phone_number = json_data.get('telephone', phone_number)
    url = website_link
    payment_methods = json_data.get('paymentAccepted', '').split(', ') if json_data.get('paymentAccepted') else []

    # Create a dictionary for DataFrame
    restaurant_data = {
        "restaurantName": restaurant_name,
        "address": address,
        "city": city,
        "postalCode": postal_code,
        "country": country,
        "priceRange": price_range,
        "cuisineType": cuisine,
        "description": description_text,
        "facilitiesServices": services_list,
        "creditCards": payment_methods,
        "phoneNumber": phone_number,
        "website": url
    }

    return restaurant_data

# Function to process all saved HTML pages and create a single DataFrame
def process_saved_pages():
    all_restaurant_data = []  # List to store all restaurant data from all pages

    page_folders = [f for f in os.listdir() if f.startswith('page')]  # List all page folders (page 1, page 2, etc.)

    for page_folder in page_folders:
        for filename in os.listdir(page_folder):
            file_path = os.path.join(page_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                # Extract data from the HTML content
                restaurant_data = extract_data_from_html(html_content)
                all_restaurant_data.append(restaurant_data)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(all_restaurant_data)
    output_filename = 'restaurant.tsv'  # Final output file name
    df.to_csv(output_filename, sep='\t', index=True, index_label="index")  # Save as tsv format
    print(f"Saved all restaurant data to {output_filename}")
    return df
