import csv
import json


def parse_txt_file(txt_file):
    """
    Parse quotes and authors from txt file. 
    Returns 2 lists: quotes and authors.
    """
    quotes = {}

    with open(txt_file, 'r') as file:
        for row in file:
            quote, author = row.rsplit(' - ', 1)
            quote = quote.strip()
            author = author.strip()
            categories = []  # No categories in txt file
            if author in quotes:
                quotes[author].append((quote, categories))
            else:
                quotes[author] = [(quote, categories)]

    return quotes


def parse_csv_file(csv_file):
    """
    Parse quotes and authors from csv file. 
    Returns Dictionary where author is the key, and quotes/categories as list values.
    """
    quotes = {}
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)   # read contents of each column into a dictionary
        for row in reader:
            quote = row['text']
            author = row['author']
            categories = row['categories'].split(',')   # split categories into a list
            if author in quotes:
                quotes[author].append((quote, categories))
            else:
                quotes[author] = [(quote, categories)]

    return quotes


def parse_json_file(json_file):
    """
    Parse quotes and authors from a JSON file.
    Returns a dictionary where the author is the key, and quotes/categories are stored as list values.
    """
    quotes = {}

    with open(json_file, 'r') as file:
        data = json.load(file)
        for entry in data:
            quote = entry['Quote']
            author = entry['Author']
            categories = entry['Category']

            if author in quotes:
                quotes[author].append((quote, categories))
            else:
                quotes[author] = [(quote, categories)]

    return quotes



# Print Stats to Terminal
def print_stats(parsed_quotes):
    """
    Print statistics based on the parsed quotes.
    """
    num_authors = len(parsed_quotes)
    num_quotes_per_author = {author: len(quotes) for author, quotes in parsed_quotes.items()}
    categories = set(category for quotes in parsed_quotes.values() for _, categories in quotes for category in categories)

    print(f"Number of authors: {num_authors}")

    # Print authors and number of quotes in alphabetical order
    num_quotes_per_author = sorted(num_quotes_per_author.items())
    print("Number of quotes per author:")
    for author, num_quotes in num_quotes_per_author:
        print(f"{author}: {num_quotes}")

    # Print categories in alphabetical order
    categories = sorted(categories)
    print("Categories (alphabetical order):")
    for category in categories:
        print(category)


def print_total_stats(parsed_quotes):
    """
    Print essential statistics based on the parsed quotes.
    """
    num_authors = len(parsed_quotes)
    num_quotes = sum(len(quotes) for quotes in parsed_quotes.values())
    categories = set(category for quotes in parsed_quotes.values() for _, categories in quotes for category in categories)
    num_categories = len(categories)

    print(f"Total number of authors: {num_authors}")
    print(f"Total number of quotes: {num_quotes}")
    print(f"Total number of categories: {num_categories}")



# Input files
txt_file = 'quotes.txt'
csv_file = 'quotes.csv'
json_file = 'quotes.json'


# txt parse
parsed_quotes_txt = parse_txt_file(txt_file)
# print_stats(parsed_quotes_txt)
print()
print("Text File")
print("---------")
print_total_stats(parsed_quotes_txt)

# csv parse
parsed_quotes_csv = parse_csv_file(csv_file)
# print_stats(parsed_quotes_csv)
print()
print("csv File")
print("---------")
print_total_stats(parsed_quotes_csv)

# json parse
parsed_quotes_json = parse_json_file(json_file)
print_stats(parsed_quotes_json)
print()
print("json File")
print("---------")
print_total_stats(parsed_quotes_json)
