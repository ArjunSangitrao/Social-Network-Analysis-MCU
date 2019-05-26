

import urllib.request
import sys
import json
import numpy as np
import os

from bs4 import BeautifulSoup


to_search = "abcdefghijklmnopqrstuvwxyz"
link = "https://www.chronologyproject.com/{}.php"

result_character_name_comics = dict()
for each in to_search:
    full_link = link.format(each)

    # Give intermediate updates
    sys.stdout.write(
            f"\rCollecting names: {to_search.index(each) + 1}/{len(to_search)}"
            f" last visited link: {full_link}")
    sys.stdout.flush()

    # Open a link and convert it with BeautifulSoup
    with urllib.request.urlopen(full_link) as response:
        html_source = response.read()
        soup = BeautifulSoup(html_source, 'html.parser')

        # Find the paragraphs containing characters
        characters = soup.find_all("p")
        for character in characters:
            if "id=" in str(character):
                if len(character.find_all("span")) == 2:
                    char, comics = character.find_all("span")

                    # Get all the comics for 1 characters
                    filters = ['See', 'From']
                    clean_comics = []
                    for comic in comics.text.strip().split("\n"):
                        for filter_ in filters:
                            if filter_ not in comic:
                                clean_comics.append(comic)

                    result_character_name_comics[char.text] = clean_comics


# This will print 5 random samples
samples = np.random.choice(list(result_character_name_comics), 5)
for num, name in enumerate(samples):
    if not num:
        print("\n\n 5 random samples:")
    print(f"{str(num).ljust(5)} {name.ljust(50)} {result_character_name_comics[name]}")

# Storing the output
if not os.path.exists("data"):
    os.mkdir("data")

file_location = os.path.join("data", "character.json")
with open("character.json", "w") as file:
    json.dump(result_character_name_comics, file)

# Summarize the results
print(f"\nCollected {len(result_character_name_comics)} character names")
