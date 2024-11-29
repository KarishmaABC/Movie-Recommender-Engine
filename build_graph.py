 
import networkx as nx

def build_similarity_graph(data):
    G = nx.Graph()
    for i, movie in data.iterrows():
        G.add_node(movie["title"], genre=movie["genre"], director=movie["director"])
        for j, other_movie in data.iterrows():
            if movie["title"] != other_movie["title"]:
                if movie["genre"] == other_movie["genre"]:  # Genre similarity
                    G.add_edge(movie["title"], other_movie["title"], weight=1.0)
    return G
