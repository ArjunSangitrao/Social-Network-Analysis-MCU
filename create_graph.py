
from collections import namedtuple
from graph import Graph

graph = Graph()
filter_times = namedtuple("filter_times", ["min", "max", "min_main"])


############################################
# Add your filters here
filter_title = []
filter_title_exclude = []

filter_name = ["HAWKEYE/CLINTON FRANCIS BARTON", "HULK", "WASP"]
filter_name_exclude = ["THUNDERBOLT"]

filter_times = filter_times(min=50,
                            max=float("inf"),
                            min_main=float("inf"))
############################################


df = graph.data
for column, filters, exclude in [("Title", filter_title, filter_title_exclude),
                                 ("Name", filter_name, filter_name_exclude)]:
    temp = [] + filters
    for row in df[column]:
        for each in filters:
            if each.upper() in str(row).upper() and str(row).upper() not in temp:
                for remove in exclude:
                    if remove.upper() in str(row).upper():
                        break
                else:
                    temp.append(row.upper())
    df[column].map(lambda x: str(x).upper())
    if temp:
        df = df.loc[df[column].isin(temp)]

df = df.loc[df["occurrences"] >= filter_times.min]
df = df.loc[df["occurrences"] <= filter_times.max]
graph.data = df

# Create the different colours we want to have and create the colour map in the Graph
graph.colour_types.extend(["Comic", "Normal character", "Main Character", "Bridge"])
graph.map_types_to_colours()


# Add the colour comic to all comics
val_map = dict()
for comic, character, occurrences in zip(df["Title"], df["Name"], df["occurrences"]):
    val_map[comic] = 'Comic'
    val_map[character] = 'Normal character'

    if occurrences > filter_times.min_main:
        val_map[character] = 'Main Character'

    if comic in ["AVENGERS", "AVENGERS VOL. 3"]:
        val_map[comic] = 'Bridge'

graph.map_key_to_values(val_map)


name = f"comics {'  '.join(filter_title)} names- {' '.join(filter_name)} " \
       f"min-{filter_times.min} max-{filter_times.max} min_main-{filter_times.min_main}"
graph.draw_graph_edges(source="Title", target="Name", attrs=["Title"],
                       show=True, store=True, name=name.replace("/", " "))
