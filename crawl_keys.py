

from bs4 import BeautifulSoup
import urllib.request
import json
import os


link = "https://www.chronologyproject.com/key.php"

results_table_code_title_date = []
results_table_title_code = []

with urllib.request.urlopen(link) as response:
    html_source = response.read()
    soup = BeautifulSoup(html_source, 'html.parser')

    tables = soup.find_all("table")
    for table in tables[2:]:
        for line in table:
            if len(line) >= 2:

                temp = []
                for column in line.findChildren("td"):
                    temp.append(column.text)

                if len(line) == 3:
                    results_table_code_title_date.append("\t".join(temp))

                if len(line) == 2:
                    results_table_title_code.append("\t".join(temp))

    extra_rows = soup.find_all("tr")
    for each in extra_rows:
        columns = each.find_all("td")
        result = "\t".join([col.text for col in columns])
        # this will remove empty lines and the keys with their long descriptions
        if len(columns) == 2 and len(columns[1]) < 50:
            results_table_title_code.append(result)


unique = []


def get_code_title():
    for num, row in enumerate(results_table_code_title_date):
        if len(row.split("\t")) != 3:
            continue

        code, title, year = row.split("\t")
        if "\t".join([code, title]) not in results_table_title_code:
            unique.append("\t".join([title, code]))

    for num, row in enumerate(unique + results_table_title_code):
        title, code = row.split('\t')
        print(f"{str(num).ljust(5)} {code.ljust(15)} {title}")

    print(f"\nFound {len(unique + results_table_title_code)} keys in total, of which {len(unique)} because of merging")

    if not os.path.exists("data"):
        os.mkdir("data")

    file_location = os.path.join("data", "comics.json")
    with open(file_location, "w") as file:
        json.dump(unique + results_table_title_code, file)


def get_code_title_year():
    for num, row in enumerate(results_table_code_title_date):
        if len(row.split("\t")) != 3:
            continue

        code, title, year = row.split("\t")
        if "\t".join([code, title]) not in results_table_title_code:
            unique.append("\t".join([title, code, year]))

    if not os.path.exists("data"):
        os.mkdir("data")

    file_location = os.path.join("data", "comics year.json")
    with open(file_location, "w") as file:
        json.dump(unique + results_table_title_code, file)


get_code_title()
# get_code_title_year()
