import re
import json
import random
import csv


# Import classes and methods from other files.
from parse_quotes_json import ParseQuotesJson
from parse_quotes_csv import ParseQuotesCsv

# Main function
def main():
    """Main function."""
    json_file = 'quotes.json'
    quotes = ParseQuotesJson(json_file)
    # print(quotes.get_unique_authors())
    # print(quotes.get_unique_tags())
    # print(quotes.get_quotes_by_author('Albert Einstein'))
    # print(quotes.get_quotes())
    # print(quotes.get_random_quote())
    # print(quotes.get_random_quote_by_author('Albert Einstein'))
    # print(quotes.get_random_quote_by_tag('love'))
    
    file_name = 'Quotes2.csv'
    quotes = ParseQuotesCsv(file_name)
    # print(quotes.get_unique_authors())
    # print(quotes.get_unique_tags())
    # print(quotes.get_quotes_by_author('Albert Einstein'))
    # print(quotes.get_quotes())
    # print(quotes.get_random_quote())
    # print(quotes.get_random_quote_by_author('Albert Einstein'))
    # print(quotes.get_random_quote_by_tag('love'))



# CLASSES

# Parse json file for quotes.
# Create a class to handle various methods for parsing quotes in json file.
# Quote format: "quote", "author", "tags"
# Class to handle parsing quotes in json file.
class ParseQuotesJson:
    """Class to handle parsing quotes in json file."""

    def __init__(self, json_file):
        """Initialize ParseQuotesJson class."""
        self.json_file = json_file

    def line_count(self):
        """Count the number of lines in a json file."""
        with open(self.json_file) as file:
            row_count = 0
            for row in file:
                row = row.strip()
                row_count += 1
            print(row_count)

    def read_file(self):
        """Read a json file."""
        with open(self.json_file) as file:
            reader = json.load(file)
            print(reader)

    def read_file_dict(self):
        """Read a json file as a dictionary."""
        with open(self.json_file) as file:
            reader = json.load(file)
            print(reader)

    def headers(self):
        """Print the headers of a json file."""
        with open(self.json_file) as file:
            reader = json.load(file)
            print(reader)

    def find_non_ascii_chars(self):
        """Find non-ASCII characters in a json file. Count lines and characters."""
        with open(self.json_file, 'r') as file:
            char_no = 0
            for line_no, line in enumerate(file, start=1):
                for char_no, char in enumerate(line, start=1):
                    if ord(char) > 127:
                        line_no += 1
                        char_no += 1
                        print(f'Non-ASCII character {char} found at line {line_no}, character {char_no}')
            print(f'Character count: {char_no}')

    def write_column(self, column_name):
        """Write a column from a json file to a csv file."""
        with open(self.json_file, 'r') as file:
            reader = json.load(file)
            with open('quotes.csv', 'w') as file:
                writer = csv.writer(file)
                for row in reader:
                    writer.writerow(row[column_name])

    def write_columns(self, column_names):
        """Write multiple columns from a json file to a csv file."""
        with open(self.json_file, 'r') as file:
            reader = json.load(file)
            with open('quotes.csv', 'w') as file:
                writer = csv.writer(file)
                for row in reader:
                    writer.writerow([row[column_name] for column_name in column_names])

    def get_unique_authors(self):
        """Get unique authors from json file."""
        with open(self.json_file, 'r') as f:
            quotes = json.load(f)
        authors = set()
        for quote in quotes:
            authors.add(quote['Author'])
        return authors
    
    def get_unique_tags(self):
        """Get unique tags from json file."""
        with open(self.json_file, 'r') as f:
            quotes = json.load(f)
        tags = set()
        for quote in quotes:
            for tag in quote['Tags']:
                tags.add(tag)
        return tags
    
    def get_quotes_by_author(self, author):
        """Get quotes by author from json file."""
        with open(self.json_file, 'r') as f:
            quotes = json.load(f)
        quotes_by_author = [quote for quote in quotes if quote['Author'] == author]
        return quotes_by_author

    def get_quotes(self):
        """Get all quotes from json file."""
        with open(self.json_file, 'r') as f:
            quotes = json.load(f)
        return quotes
    
    def get_random_quote(self):
        """Get random quote from json file."""
        quotes = self.get_quotes()
        quote = random.choice(quotes)
        return quote
    
    def get_random_quote_by_author(self, author):
        """Get random quote by author from json file."""
        quotes = self.get_quotes()
        quotes_by_author = [quote for quote in quotes if quote['Author'] == author]
        quote = random.choice(quotes_by_author)
        return quote
    
    def get_random_quote_by_tag(self, tag):
        """Get random quote by tag from json file."""
        quotes = self.get_quotes()
        quotes_by_tag = [quote for quote in quotes if tag in quote['Tags']]
        quote = random.choice(quotes_by_tag)
        return quote


# Main function
def main():
    """Main function."""
    # json_file = os.path.join(sys.path[0], 'quotes.json')
    json_file = 'quotes.json'
    quotes = ParseQuotesJson(json_file)
    # quotes.line_count()
    # quotes.read_file()
    # quotes.read_file_dict()
    # quotes.headers()
    # quotes.find_non_ascii_chars()
    # authors = quotes.get_unique_authors()
    # print(authors)
    # tags = quotes.get_unique_tags()
    # print(tags)
    # quotes_by_author = quotes.get_quotes_by_author('Dr. Seuss')
    # print(quotes_by_author)
    # quotes = quotes.get_quotes()
    # print(quotes)
    # quote = quotes.get_random_quote()
    # print(quote)
    # quote = quotes.get_random_quote_by_author('Albert Einstein')
    # print(quote)
    quote = quotes.get_random_quote_by_tag('love')
    print(quote)



# Parse csv file for quotes.
# Create a class to handle various methods for parsing quotes in csv file.
# Quote format: "quote", "author", "tags"
class ParseQuotesCsv:
    """Class to handle parse quotes in csv file."""

    def __init__(self, file_name):
        """Initialize ParseQuotesCsv class."""
        self.file_name = file_name

    def find_non_ascii_chars(self):
        """Find non-ASCII characters in a csv file. Count lines and characters."""
        with open(self.file_name, 'r') as file:
            char_no = 0
            for line_no, line in enumerate(file, start=1):
                for char_no, char in enumerate(line, start=1):
                    if ord(char) > 127:
                        line_no += 1
                        char_no += 1
                        print(f'Non-ASCII character {char} found at line {line_no}, character {char_no}')
            print(f'Character count: {char_no}')

    def line_count(self):
        """Count the number of lines in a csv file."""
        with open(self.file_name) as file:
            row_count = 0
            for row in file:
                row = row.strip()
                row_count += 1
            print(row_count)

    def column_count(self):
        """Count the number of columns in a csv file."""
        with open(self.file_name) as file:
            column_count = 0
            for row in file:
                row = row.strip()
                column_count = len(row.split(','))
            print(column_count)

    def read_file(self):
        """Read a csv file."""
        with open(self.file_name) as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)

    def read_file_dict(self):
        """Read a csv file as a dictionary."""
        with open(self.file_name) as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)

    def headers(self):
        """Print the headers of a csv file."""
        with open(self.file_name) as file:
            reader = csv.DictReader(file)
            print(reader.fieldnames)

    def write_column(self, column_name):
        """Write unique column fields of a csv file to a new csv file. Order by alphabetical order of fields."""
        written_values = set()
        with open(self.file_name) as file:
            reader = csv.DictReader(file)
            with open('column_data.csv', 'w') as new_file:
                writer = csv.writer(new_file)
                for row in reader:
                    if row[column_name] not in written_values:
                        writer.writerow([row[column_name]])
                        written_values.add(row[column_name])

    def write_rows(self, author_name):
        """Write specific rows of a csv file to a new csv file."""
        with open(self.file_name) as file:
            reader = csv.DictReader(file)
            with open('author_quotes.csv', 'w') as new_file:
                writer = csv.writer(new_file)
                for row in reader:
                    if row['Author'] == author_name:
                        writer.writerow((row['Quote'], row['Author'], row['Tags']))

    def get_unique_authors(self):
        """Get unique authors from csv file."""
        with open(self.file_name, 'r') as file:
            quotes = csv.DictReader(file)
        authors = set()
        for quote in quotes:
            authors.add(quote['Author'])
        return authors
    
    def get_unique_tags(self):
        """Get unique tags from csv file."""
        with open(self.file_name, 'r') as file:
            quotes = csv.DictReader(file)
        tags = set()
        for quote in quotes:
            for tag in quote['Tags']:
                tags.add(tag)
        return tags
    
    def get_quotes_by_author(self, author):
        """Get quotes by author from csv file."""
        with open(self.file_name, 'r') as file:
            quotes = csv.DictReader(file)
        quotes_by_author = [quote for quote in quotes if quote['Author'] == author]
        return quotes_by_author
    
    def get_quotes(self):
        """Get all quotes from csv file."""
        with open(self.file_name, 'r') as file:
            quotes = csv.DictReader(file)
        return quotes
    
    def get_random_quote(self):
        """Get random quote from csv file."""
        quotes = self.get_quotes()
        quote = random.choice(quotes)
        return quote
    
    def get_random_quote_by_author(self, author):
        """Get random quote by author from csv file."""
        quotes = self.get_quotes()
        quotes_by_author = [quote for quote in quotes if quote['Author'] == author]
        quote = random.choice(quotes_by_author)
        return quote
    
    def get_random_quote_by_tag(self, tag):
        """Get random quote by tag from csv file."""
        quotes = self.get_quotes()
        quotes_by_tag = [quote for quote in quotes if tag in quote['Tags']]
        quote = random.choice(quotes_by_tag)
        return quote
    

# Main function
def main():
    """Main function."""
    file_name = 'quotes.csv'
    quotes = ParseQuotesCsv(file_name)
    # quotes.find_non_ascii_chars()
    # quotes.line_count()
    # quotes.column_count()
    # quotes.read_file()
    # quotes.read_file_dict()
    # quotes.headers()
    # quotes.write_column('Author')
    # quotes.write_rows('Albert Einstein')
    # print(quotes.get_unique_authors())
    # print(quotes.get_unique_tags())
    # print(quotes.get_quotes_by_author('Albert Einstein'))
    # print(quotes.get_quotes())
    # print(quotes.get_random_quote())
    # print(quotes.get_random_quote_by_author('Albert Einstein'))
    # print(quotes.get_random_quote_by_tag('inspirational'))

# Run program
if __name__ == '__main__':
    main()
