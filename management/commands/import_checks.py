# Checks if the import_quotes.py file is working properly.
# Path: management/commands/import_quotes.py

# Run program command: 
# python manage.py import_checks

# Redirect output to txt file command:
# python manage.py import_checks > import_checks.txt    # Overwrites the file
# python manage.py import_checks >> import_checks.txt    # Appends to the file

# Silence output command:
# python manage.py import_checks > /dev/null

# Import classes and methods from other files (import_checks.py is a subclass of Django's BaseCommand class)
from django.core.management.base import BaseCommand, CommandError
from .import_quotes import ParseQuotesTxt, ParseQuotesJson, ParseQuotesCsv
import os


# Create a class that extends BaseCommand
class Command(BaseCommand):
    help = 'Checks if the import_quotes.py file is working properly.'

    def handle(self, *args, **options):
        # Get txt file and print out the results
        txt_file = 'quotes.txt'
        if not os.path.exists(txt_file):
            raise CommandError(f'The file "{txt_file}" does not exist.')
        try:
            quotes = ParseQuotesTxt(txt_file)
            self.stdout.write(str(quotes.get_unique_authors()))
            self.stdout.write(str(quotes.get_unique_tags()))
            self.stdout.write(str(quotes.get_quotes_by_author('Albert Einstein')))
            self.stdout.write(str(quotes.get_quotes()))
            self.stdout.write(str(quotes.get_random_quote()))
            self.stdout.write(str(quotes.get_random_quote_by_author('Albert Einstein')))
            self.stdout.write(str(quotes.get_random_quote_by_tag('love')))
        except Exception as e:
            raise CommandError(f'An error occurred while processing "{txt_file}": {str(e)}')

        # Get json file and print out the results
        json_file = 'quotes.json'
        if not os.path.exists(json_file):
            raise CommandError(f'The file "{json_file}" does not exist.')
        try:
            quotes = ParseQuotesJson(json_file)
            self.stdout.write(str(quotes.get_unique_authors()))
            self.stdout.write(str(quotes.get_unique_tags()))
            self.stdout.write(str(quotes.get_quotes_by_author('Albert Einstein')))
            self.stdout.write(str(quotes.get_quotes()))
            self.stdout.write(str(quotes.get_random_quote()))
            self.stdout.write(str(quotes.get_random_quote_by_author('Albert Einstein')))
            self.stdout.write(str(quotes.get_random_quote_by_tag('love')))
        except Exception as e:
            raise CommandError(f'An error occurred while processing "{json_file}": {str(e)}')
        
        # Get csv file and print out the results
        csv_file = 'Quotes2.csv'
        if not os.path.exists(csv_file):
            raise CommandError(f'The file "{csv_file}" does not exist.')
        try:
            quotes = ParseQuotesCsv(csv_file)
            self.stdout.write(str(quotes.get_unique_authors()))
            self.stdout.write(str(quotes.get_unique_tags()))
            self.stdout.write(str(quotes.get_quotes_by_author('Albert Einstein')))
            self.stdout.write(str(quotes.get_quotes()))
            self.stdout.write(str(quotes.get_random_quote()))
            self.stdout.write(str(quotes.get_random_quote_by_author('Albert Einstein')))
            self.stdout.write(str(quotes.get_random_quote_by_tag('love')))
        except Exception as e:
            raise CommandError(f'An error occurred while processing "{csv_file}": {str(e)}')
