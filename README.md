
# Reconstructing data set

## Characters

By running 'crawl_characters.py' the website ' "https://www.chronologyproject.com/{}.php' 
will be crawled with the '{}' replaced by all 26 letters in the alphabet. 

The script will search for the characters id and then for the codes of the scripts 
in which this character appears. Sometimes there is an additional text saying:
'See also ...' or 'From ...', these are filtered out.

Then all the results are temporary stored in json files (serializable text format).
After running you should have 15.615 characters and a list containing the comic
code and occurrences in that comic.


## Comics

By running 'crawl_keys.py' the tables on "https://www.chronologyproject.com/key.php"
will be crawled, selecting the third and fourth table. Since there was be a difference 
between the tables we merge the two tables, after running you should have 5023 comic and code pairs.

## Creating CSV

Move to the data folder, this will have a 'set_json_t_csv.py', which will store both
json files as a csv file and merge the two json files into a single csv file, 
that will contain the edges.

## Building the network ...
 TODO
