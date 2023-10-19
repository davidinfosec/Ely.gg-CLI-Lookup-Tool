import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import argparse
import time
from asciichartpy import plot
import matplotlib.pyplot as plt
import webbrowser

def scrape_wallet_data(search_item):
    url = f"https://www.ely.gg/search?search_item={search_item}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        wallet_data = []

        aside_elements = soup.find_all('aside', class_='aside')

        for aside_element in aside_elements:
            date_element = aside_element.find('div', class_='center-recent').find('h4')
            day_element = aside_element.find('div', class_='center-recent').find('p')
            price_element = aside_element.find('img', {'src': '/static/assets/ex-icons/chart/gp.png', 'class': 'jvpxll'}).find_next('h4').find_next('h4')
            name_element = price_element.find_next('p', class_='smaller-font')

            if date_element and day_element and price_element and name_element:
                date = date_element.text.strip()
                day = day_element.text.strip()
                price = price_element.text.strip()
                name = name_element.text.strip()

                wallet_data.append([date, day, price, name])

        return wallet_data

    else:
        return None

def format_data(data, search_item, brief):
    formatted_data = []
    if brief:
        data = data[:10]  # Display only the latest 10 prices
    for item in data:
        formatted_item = f"{item[3]} Price | {item[2]} | Instant Sold | {item[0]} {item[1]}"
        formatted_data.append(formatted_item)
    return formatted_data

def plot_chart(prices, search_input):
    chart_data = [float(price.replace(',', '').replace(' GP', '')) for price in prices]

    # Create the chart
    plt.plot(chart_data)

    # Generate chart name based on search term, current time, and date
    now = datetime.now()
    time_code = now.strftime("%H%M")
    date_code = now.strftime("%m-%d-%Y")
    chart_name = f"chart_{search_input}_{time_code}_{date_code}.png"

    # Save the chart as an image file
    plt.savefig(chart_name)

    if args.popup:
        # Open the chart in a web browser
        webbrowser.open(chart_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve RS3 item prices from Ely.')
    parser.add_argument('item', type=str, help='The item to search for')
    parser.add_argument('-b', '--brief', action='store_true', help='Display only the latest 10 prices')
    parser.add_argument('-c', '--chart', action='store_true', help='Display a line chart of prices')
    parser.add_argument('-p', '--popup', action='store_true', help='Open the chart image in a popup')

    args = parser.parse_args()
    search_input = args.item.replace(' ', '+')
    
    wallet_data = scrape_wallet_data(search_input)

    if wallet_data:
        formatted_data = format_data(wallet_data, search_input, args.brief)
        if args.chart:
            prices = [item.split('|')[1].strip() for item in formatted_data]
            chart_name = plot_chart(prices, search_input)
            print(f"Chart saved as '{chart_name}'")
        for data in formatted_data:
            print(data)
    else:
        print("Error fetching data.")
