import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_filtered_urls(main_url, date):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    urls = []
    table = soup.find('table', class_='dataTable')
    if table:
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if cells:
                date_text = cells[0].get_text(strip=True)
                try:
                    date_parsed = datetime.strptime(date_text, '%Y-%m-%d').date()
                    if date_parsed == date:
                        link = cells[1].find('a')['href']
                        # Ensure the relative path is correctly appended
                        full_url = f"https://apps.web.maine.gov/online/aeviewer/ME/40/{link}"
                        urls.append(full_url)
                except ValueError:
                    continue
    return urls


def parse_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}
    for li in soup.find_all('li'):
        text = li.get_text(strip=True)
        parts = text.split(':', 1)
        if len(parts) == 2:
            label, value = parts
            data[label.strip()] = value.strip()

    keys_of_interest = [
        "Entity Name",
        "Description of the Breach",
        "Total number of persons affected (including residents)",
        "Date(s) Breach Occured",  # Corrected key
        "Date Breach Discovered",
        "Date(s) of consumer notification"
    ]
    values = [data.get(key, 'Not found') for key in keys_of_interest]

    return values


def fetch_and_print_details(urls):
    for url in urls:
        try:
            details = parse_webpage(url)
            print(f'{details[0]} @ is writing a breach notification letters to a subset of individuals after xyz. {details[2]} victims. Breach Occurred: {details[3]}, '
                  f'Breach Discovered: {details[4]}, Customer Notification: {details[5]}. We grade their response a xyz. #CNL #cybernewslive #cyber #')
        except Exception as e:
            print(f"Error fetching details from {url}: {e}")


# Main URL of the list page
main_url = 'https://apps.web.maine.gov/online/aeviewer/ME/40/list.shtml'
date = datetime(2024, 6, 10).date()  # Specify the date you're interested in

# Get URLs for the specified date
filtered_urls = get_filtered_urls(main_url, date)

# Fetch and print details for each URL
fetch_and_print_details(filtered_urls)
