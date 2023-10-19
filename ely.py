import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import argparse
import time
import matplotlib.pyplot as plt
import webbrowser
import os

def scrape_wallet_data(search_item):
    url = f"https://www.ely.gg/search?search_item={search_item}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        wallet_data = []

        aside_elements = soup.find_all('aside', class_='aside')

        now = datetime.now()
        current_year = now.year

        for aside_element in aside_elements:
            date_element = aside_element.find('div', class_='center-recent').find('h4')
            day_element = aside_element.find('div', class_='center-recent').find('p')
            price_element = aside_element.find('img', {'src': '/static/assets/ex-icons/chart/gp.png', 'class': 'jvpxll'}).find_next('h4').find_next('h4')
            name_element = price_element.find_next('p', class_='smaller-font')
            trade_type_element = price_element.find_previous('h4', class_='cicsNy kBzJqa czMglK')

            if date_element and day_element and price_element and name_element:
                date_text = date_element.text.strip()
                day = day_element.text.strip()
                price = price_element.text.strip()
                name = name_element.text.strip()

                if trade_type_element:
                    trade_type = trade_type_element.text.strip()
                else:
                    trade_type = "Unknown"

                date_parts = date_text.split('-')
                month = datetime.strptime(date_parts[0], '%B').month
                if month > now.month:
                    approx_year = current_year - 1
                else:
                    approx_year = current_year

                wallet_data.append([date_text, day, price, name, trade_type, approx_year])

        # Sort wallet_data based on date in descending order (newest at the top)
        wallet_data.sort(key=lambda x: (x[5], x[0]), reverse=True)

        return wallet_data

    else:
        return None

def format_data(data, search_item, brief):
    formatted_data = []
    if brief:
        data = data[:10]  # Display only the latest 10 prices
    for item in data:
        date = item[0]
        day = item[1]
        price_element = item[2]
        name = item[3]
        trade_type = item[4]
        approx_year = item[5]

        formatted_item = f"{name} | {price_element} | {trade_type} | {date} {day} {approx_year}"
        formatted_data.append(formatted_item)
    return formatted_data

def plot_combined_chart(prices, search_input, item_name, time_code, dates):
    chart_data = [float(price.replace(',', '').replace(' GP', '')) for price in prices]

    now = datetime.now()
    date_code = now.strftime("%m-%d-%Y")
    chart_name = f"chart_{search_input}_{time_code}_{date_code}.png"

    if not os.path.exists('charts'):
        os.makedirs('charts')

    if not os.path.exists(os.path.join('charts', date_code)):
        os.makedirs(os.path.join('charts', date_code))

    item_folder = os.path.join('charts', date_code, item_name[4:].replace('price', '').strip())
    if not os.path.exists(item_folder):
        os.makedirs(item_folder)

    # Reverse the order of chart_data
    chart_data.reverse()

    plt.figure(figsize=(10, 5))  # Adjust figure size
    plt.rcParams.update({'font.size': 8})  # Adjust font size

    plt.plot(chart_data)
    plt.title(f"{item_name.replace('+', ' ')} Price Chart")
    plt.xlabel("Data Point")
    plt.ylabel("Price (in GP)")

    # Define custom y-axis labels with more precision
    y_labels = ['{:.3f}B'.format(x / 1000000000) if x >= 1000000000
                else '{:.3f}M'.format(x / 1000000) if x >= 1000000
                else '{:.3f}K'.format(x / 1000) if x >= 1000
                else '{:.0f}'.format(x)
                for x in plt.gca().get_yticks()]

    plt.yticks(plt.gca().get_yticks(), labels=y_labels)

    # Add text for month/year below the data points
    for i, price in enumerate(prices):
        elements = price.split('|')
        if len(elements) >= 4:  # Ensure the data point has the required elements
            month_year = elements[3].strip()
            plt.text(i, -0.15, month_year, ha='center', transform=plt.gca().transData, rotation=45)  # Rotate labels

    # Set x-axis ticks and labels
    plt.xticks(range(len(prices)), dates, rotation=45, ha='right')
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))  # Set a fixed number of ticks

    chart_path = os.path.join(item_folder, chart_name)

    plt.tight_layout()  # Adjust layout
    plt.savefig(chart_path)

    return chart_path

def process_item(item):
    search_input = item.replace(' ', '+')
    wallet_data = scrape_wallet_data(search_input)

    if wallet_data:
        formatted_data = format_data(wallet_data, search_input, args.brief)
        if args.chart:
            prices = [item.split('|')[1].strip() for item in formatted_data]
            dates = [item.split('|')[3].strip() for item in formatted_data][::-1]
            item_name = formatted_data[0].split('|')[0].strip()
            now = datetime.now()
            time_code = now.strftime("%H%M%S")
            chart_name = plot_combined_chart(prices, search_input, item_name, time_code, dates)
            print(f"Chart for {item_name} saved as '{chart_name}'")
            if args.popup:
                webbrowser.open(chart_name)

        for data in formatted_data:
            print(data)
    else:
        print(f"Error fetching data for {item}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve RS3 item prices from Ely.')
    parser.add_argument('items', type=str, nargs='+', help='The items to search for')
    parser.add_argument('-b', '--brief', action='store_true', help='Display only the latest 10 prices')
    parser.add_argument('-c', '--chart', action='store_true', help='Display a line chart of prices')
    parser.add_argument('-p', '--popup', action='store_true', help='Open the chart image in a popup')

    args = parser.parse_args()

    for item in args.items:
        process_item(item)
        time.sleep(1)  # Adjust the delay as needed (in seconds)
