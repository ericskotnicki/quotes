# Contains Classes and methods for inserting quotes, authors and tags into Django db.
# Contains additional Classes and methods for parsing quotes from each file to check if the import_quotes.py file is working properly.
# Path: management/commands/import_quotes.py

# File Types: txt, json, csv
# Quote Formats:
# txt: "quote" - author
# json: {"Quote": "quote", "Author": "author", "Tags": ["tag1", "tag2"], "Category": "category"}
# csv: Headers = Quote,Author,Tags;  Format = "quote",author,"tag1, tag2" or 'quote',author,"tag1, tag2" or quote,author,"tag1, tag2"

# Import modules
from django.core.management.base import BaseCommand, CommandError
from quote.models import Quote, Author, Tag, Category
import os, csv, json, random, sys, re


# Insert quotes, authors and tags into Django db
def insert_quotes(file):
    """Insert quotes, authors, tags and category into Django db."""
    # Get file extension, raise error if not supported (txt, json, csv)
    file_extension = os.path.splitext(file)[1]

    #  txt file
    if file_extension == '.txt':
        with open(file, 'r') as f:
            lines_ignored = 0   # Count ignored quotes
            lines_parsed = 0   # Count total quotes
            for line in file:
                line = line.strip() # Remove leading and trailing whitespace
                # Skip lines that don't contain ' - ' to avoid errors
                if ' - ' not in line:
                    print(f'Line ignored: {line}')
                    count_ignored += 1  # Increment ignored quotes
                    continue
                # Parse quote and author
                quote, author = line.rsplit(' - ', maxsplit=1)  # Split at last occurrence of ' - ' to avoid splitting the quote
                total_parsed += 1   # Increment total quotes

                # Insert quote and author into db
                quote = Quote(text=quote, author=author)
                quote.save()

                # Insert tags into db
                # if tags:
                #     for tag in tags:
                #         tag = Tag(name=tag)
                #         tag.save()
                #         quote.tags.add(tag)
                # quote.save()

            # Print results
            print(f'Number of lines parsed: {lines_parsed}')
            print(f'Number of quotes ignored: {lines_ignored}')
            print(f'Quotes added to db: {lines_parsed - lines_ignored}')
        
        file.close()    # Close file
            

    # json file
    elif file_extension == '.json':
        with open(file, 'r') as f:
            # Read json file
            reader = json.load(f)
            # Parse json file
            for row in reader:
                # Insert quote and author into db
                quote = Quote(text=row['Quote'], author=row['Author'], category=row['Category'])
                quote.save()
                author = Author(name=row['Author'])
                category = Category(name=row['Category'])
                category.save()
                quote.category.add(category)
                # Insert tags into db
                if row['Tags']:
                    for tag in row['Tags']:
                        tag = Tag(name=tag)
                        tag.save()
                        quote.tags.add(tag)
                quote.save()

            # Print number of quotes added to db
            print(f'Quotes added to db: {len(reader)}')

        file.close()    # Close file
            

    # csv file
    elif file_extension == '.csv':
        with open(file, 'r') as f:
            # Read csv file
            reader = csv.DictReader(f)
            # Parse csv file
            for row in reader:
                # Insert quote and author into db
                quote = Quote(text=row['Quote'], author=row['Author'])
                quote.save()
                # Insert tags into db
                if row['Tags']:
                    for tag in row['Tags']:
                        tag = Tag(name=tag)
                        tag.save()
                        quote.tags.add(tag)
                quote.save()

            # Print number of quotes added to db
            print(f'Quotes added to db: {len(reader)}')

        file.close()    # Close file

    else:
        raise CommandError(f'File extension "{file_extension}" is not supported.') 



# Create a class that extends BaseCommand
class Command(BaseCommand):
    help = 'Inserts quotes, authors and tags into Django db.'

    def handle(self, *args, **options):

        # Get txt file and insert into db
        txt_file = 'quotes.txt'
        if not os.path.exists(txt_file):
            raise CommandError(f'The file "{txt_file}" does not exist.')
        try:
            insert_quotes(txt_file)
        except Exception as e:
            raise CommandError(f'An error occurred while processing "{txt_file}": {str(e)}')
        
        # Get json file and insert into db
        json_file = 'quotes.json'
        if not os.path.exists(json_file):
            raise CommandError(f'The file "{json_file}" does not exist.')
        try:
            insert_quotes(json_file)
        except Exception as e:
            raise CommandError(f'An error occurred while processing "{json_file}": {str(e)}')
        
        # Get csv file and insert into db
        csv_file = 'Quotes2.csv'
        if not os.path.exists(csv_file):
            raise CommandError(f'The file "{csv_file}" does not exist.')
        try:
            insert_quotes(csv_file)
        except Exception as e:
            raise CommandError(f'An error occurred while processing "{csv_file}": {str(e)}')
        
    

class ParseQuotesTxt:
    """Class to handle parsing quotes in a txt file."""
    def __init__(self, txt_file):
        """Initialize ParseQuotesTxt class."""
        self.txt_file = txt_file

    def line_count(self):
        """Count the number of lines in a txt file."""
        with open(self.txt_file) as file:
            row_count = 0
            for row in file:
                row = row.strip()
                row_count += 1
            print(row_count)

    def read_file(self):
        """Read a txt file."""
        with open(self.txt_file) as file:
            reader = file.readlines()
            print(reader)

    def read_file_dict(self):
        """Read a txt file as a dictionary."""
        with open(self.txt_file) as file:
            reader = file.readlines()
            print(reader)

    def headers(self):
        """Print the headers of a txt file."""
        with open(self.txt_file) as file:
            reader = file.readlines()
            print(reader)

    def find_non_ascii_chars(self):
        """Find non-ASCII characters in a txt file. Count lines and characters."""
        with open(self.txt_file, 'r') as file:
            char_no = 0
            for line_no, line in enumerate(file, start=1):
                for char_no, char in enumerate(line, start=1):
                    if ord(char) > 127:
                        line_no += 1
                        char_no += 1
                        print(f'Non-ASCII character {char} found at line {line_no}, character {char_no}')
            print(f'Character count: {char_no}')

    def write_column(self, column_name):
        """Write a column from a txt file to a csv file."""
        with open(self.txt_file, 'r') as file:
            reader = file.readlines()
            with open('quotes.csv', 'w') as file:
                writer = csv.writer(file)
                for row in reader:
                    writer.writerow(row[column_name])

    def write_columns(self, column_names):
        """Write multiple columns from a txt file to a csv file."""
        with open(self.txt_file, 'r') as file:
            reader = file.readlines()
            with open('quotes.csv', 'w') as file:
                writer = csv.writer(file)
                for row in reader:
                    writer.writerow([row[column_name] for column_name in column_names])

    def get_unique_authors(self):
        """Get unique authors from txt file."""
        with open(self.txt_file, 'r') as file:
            quotes = file.readlines()
        authors = set()
        for quote in quotes:
            authors.add(quote.split(',')[1])
        return authors
    
    def get_quotes_by_author(self, author):
        """Get quotes by author from txt file."""
        with open(self.txt_file, 'r') as file:
            quotes = file.readlines()
        quotes_by_author = [quote for quote in quotes if quote.split(',')[1] == author]
        return quotes_by_author
    
    def get_quotes(self):
        """Get all quotes from txt file."""
        with open(self.txt_file, 'r') as file:
            quotes = file.readlines()
        return quotes
    
    def get_random_quote(self):
        """Get random quote from txt file."""
        quotes = self.get_quotes()
        quote = random.choice(quotes)
        return quote
    
    def get_random_quote_by_author(self, author):
        """Get random quote by author from txt file."""
        quotes = self.get_quotes()
        quotes_by_author = [quote for quote in quotes if quote.split(',')[1] == author]
        quote = random.choice(quotes_by_author)
        return quote
    


class ParseQuotesJson:
    """Class to handle parsing quotes in a json file."""
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



class ParseQuotesCsv:
    """Class to handle parsing quotes in a csv file."""
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
    

"""
def main():
    json_file = os.path.join(sys.path[0], 'quotes.json')
    json_file = 'quotes.json'
    quotes = ParseQuotesJson(json_file)
    quotes.line_count()
    quotes.read_file()
    quotes.read_file_dict()
    quotes.headers()
    quotes.find_non_ascii_chars()
    authors = quotes.get_unique_authors()
    print(authors)
    tags = quotes.get_unique_tags()
    print(tags)
    quotes_by_author = quotes.get_quotes_by_author('Dr. Seuss')
    print(quotes_by_author)
    quotes = quotes.get_quotes()
    print(quotes)
    quote = quotes.get_random_quote()
    print(quote)
    quote = quotes.get_random_quote_by_author('Albert Einstein')
    print(quote)
    quote = quotes.get_random_quote_by_tag('love')
    print(quote)
    

def main():
    file_name = 'quotes.csv'
    quotes = ParseQuotesCsv(file_name)
    quotes.find_non_ascii_chars()
    quotes.line_count()
    quotes.column_count()
    quotes.read_file()
    quotes.read_file_dict()
    quotes.headers()
    quotes.write_column('Author')
    quotes.write_rows('Albert Einstein')
    print(quotes.get_unique_authors())
    print(quotes.get_unique_tags())
    print(quotes.get_quotes_by_author('Albert Einstein'))
    print(quotes.get_quotes())
    print(quotes.get_random_quote())
    print(quotes.get_random_quote_by_author('Albert Einstein'))
    print(quotes.get_random_quote_by_tag('inspirational'))


Run program
if __name__ == '__main__':
    main()
"""