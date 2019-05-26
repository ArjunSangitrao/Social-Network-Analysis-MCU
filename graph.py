
import pandas
import os
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np


class Graph:
    def __init__(self):
        file_loc = os.path.join("data", "character_comic.csv")
        self.data = self.load_data_from_csv(file_loc)
        print("Loaded default data 'character_comic.csv', you can load own dataset"
              "using 'load_data_from_csv(file_name=)'.")

        self.colour_types = []
        self.colour_type_value_map = dict()
        self.colour_cmap = dict()

    @staticmethod
    def load_data_from_csv(file_name):
        """  Returns a dataframe from a csv file.  """
        assert file_name.endswith(".csv"), "Please insert a csv file"
        assert os.path.exists(file_name), f"file {file_name} does not exist"

        return pandas.read_csv(file_name)

    def map_types_to_colours(self):
        """ Returns type and value for mapping.  """
        assert self.colour_types, "First append some colour types"

        cmap = plt.get_cmap('viridis')
        colours = cmap(np.linspace(0, 1, len(self.colour_types)))
        self.colour_type_value_map = {colour: value for colour, value in zip(self.colour_types, colours)}
        return self.colour_type_value_map

    def map_key_to_values(self, value_dictionary):
        """ Append key and colour combinations you would like to add.  """
        for key, value in value_dictionary.items():
            if value in self.colour_type_value_map:
                self.colour_cmap[key] = self.colour_type_value_map[value]
            else:
                self.colour_cmap[key] = value
        return self.colour_cmap

    def draw_graph_edges(self, source, target, attrs, show=True, store=False, name="default.png"):
        """ Draw the graph from a pandas dataframe.  """

        # Create a graph
        graph = nx.from_pandas_edgelist(self.data, source, target, attrs)
        print(self.data[["Title", "Name", "occurrences"]].to_string())

        # Map the nodes to the correct colours
        if not self.colour_type_value_map:
            self.map_types_to_colours()

        values = [self.colour_cmap.get(node, 0.25) for node in graph.nodes()]

        # Draw the graph, with the colour map values
        nx.draw(graph,
                cmap=plt.get_cmap('viridis'),
                node_color=values,
                node_size=50,
                font_size=5,
                with_labels=zip(self.data[source].to_list(),
                                self.data[target].to_list()))

        if store:
            # Store with high dpi
            plt.savefig(os.path.join("images", f'{name}.png'), format='png', dpi=900)

        if show:
            plt.show()
        return self
