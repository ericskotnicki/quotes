# Handles the markdown files for the authors

# Import required libraries
import re
import os
# import markdown2

# Importing Django libraries
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage



def list_entries():
    """
    Returns a list of all names of authors from the markdown files.
    """
    _, filenames = default_storage.listdir("author")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(author, content):
    """
    Saves an author markdown, given the author's name and Markdown
    content. If an existing entry with the same author/title already exists,
    it is replaced.
    """
    filename = f"author/{author}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(author):
    """
    Retrieves a markdown file by the author's name. If no such
    file exists, the function returns None.
    """
    try:
        f = default_storage.open(f"author/{author}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None