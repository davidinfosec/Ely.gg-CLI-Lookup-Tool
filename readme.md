# Ely.gg CLI Lookup

## Overview
The Unofficial Ely.gg CLI Lookup is a Python tool designed to retrieve RuneScape 3 (RS3) item prices from the Ely gaming website. It utilizes web scraping techniques to extract relevant information and provide users with up-to-date pricing data.

## Features
- Retrieves RS3 item prices based on user input.
- Supports optional brief mode to display only the latest 10 prices.
- Outputs formatted results for easy consumption.

## Prerequisites
To use the Ely.gg CLI Lookup, you'll need the following:
- Python 3.x installed on your system.
- Required Python packages: `requests` and `beautifulsoup4`

You can install these dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Tool

The RS3 Item Price Scraper is a command-line tool. It accepts the following arguments:

- `item`: The RS3 item to search for.
- `-b`, `--brief`: Display only the latest 10 prices (optional).
- `-c`, `--chart`: Generate a .png file displaying a small chart to accompany your search.
- `-p`, `--popup`: Opens the generated .png file immediately after being generated.
- `-id`, `--itemid`: Provide item id as substition for an item name, (80 for Santa Hat, as an example)

To execute the tool, run the following command in your terminal:

```bash
python ely.py
```

### Example Usage

```bash
python ely.py
```

https://github.com/davidinfosec/Ely.gg-CLI-Lookup-Tool/assets/87215831/8dc18b7d-84c1-48a1-a8ce-4b78a9236cda
![Example - Red Partyhat longterm chart](https://i.imgur.com/oWwmpou.png)
![Example - Red Partyhat brief chart](https://i.imgur.com/VS5EzIu.png)

















### Support and Contributions

If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Your contributions are highly appreciated.

#### Disclaimer

This tool is for educational and informational purposes only. Use it responsibly and in compliance with the terms of service of the Ely website.

Disclaimer: This tool is not affiliated with or endorsed by RuneScape, Ely, or any related entities. Use at your own risk.

Feel like this has been useful? Donate toward my latest projects. https://www.poof.io/tip/@davidinfosec
