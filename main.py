import numpy as np
import networkx as nx
import json
import js
from itertools import chain
from js import input_fixed

input = input_fixed
__builtins__.input = input_fixed


def spinor(theta, phi):
    return (np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2))


def analyzer(spinor, orientation, P_in):
    """
    Stern-Gerlach analyzer
    :param spinor: tuple (a, b) - spin state
    :param orientation: tuple (theta, phi) - analyzer orientation
    :param P_in: input probability
    :return: dict
    """
    a, b = spinor
    theta, phi = orientation

    spinor_up = (np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2))
    spinor_down = (np.sin(theta/2), -np.exp(-1j*phi)*np.cos(theta/2))
    P_up = np.absolute(a*np.cos(theta/2) + b*np.sin(theta/2)*np.exp(-1j*phi))**2
    P_down = np.absolute(a*np.sin(theta/2) - b*np.cos(theta/2)*np.exp(-1j*phi))**2

    output = {"up":(spinor_up, P_in*P_up), "down":(spinor_down, P_in*P_down)}
    return output

class dict_add(dict):
    def __add__(self, other):
        dico = {}
        for key, val in chain(self.items(), other.items()):
            dico[key] = val
        return dict_add(dico)


def graph(recursive_depth=0, binary_label=""):
    G = nx.DiGraph()
    dico = dict_add({})
    print(f"current position in tree: {recursive_depth}{binary_label}")
    component = input("Component to add (A or D): ")

    node_id = f"{recursive_depth}{binary_label}"

    if component == "A":
        component_to_angles = {"X":(np.pi/2, 0), "Y":(np.pi/2, np.pi/2), "Z":(0, np.pi)}
        orientation = input("Analyzer orientation (X, Y, Z or angles): ")
        if orientation in ("X", "Y", "Z"):
            orientation = component_to_angles[orientation]
        else:
            liste = orientation.split()
            orientation = (float(liste[0]), float(liste[1]))
        recursive_depth_next = recursive_depth + 1

        G.add_node(node_id)
        dico[node_id] = orientation

        binary_label_up = binary_label + "1"
        H_up, dico_up = graph(recursive_depth_next, binary_label_up)
        G.add_nodes_from(H_up)
        G.add_edges_from(H_up.edges)
        G.add_edge(node_id, f"{recursive_depth_next}{binary_label_up}")
        dico += dico_up

        binary_label_down = binary_label + "0"
        H_down, dico_down = graph(recursive_depth_next, binary_label_down)
        G.add_nodes_from(H_down)
        G.add_edges_from(H_down.edges)
        G.add_edge(node_id, f"{recursive_depth_next}{binary_label_down}")
        dico += dico_down

    if component == "D":

        G.add_node(node_id)

    return G, dico


def local_computation(spinor, P_in, G, dico_orientation, node_id="0"):
    dico_probability = dict_add({})
    orientation = dico_orientation.get(node_id)

    if not orientation:
        dico_probability[node_id] = P_in

    for node_id in G.succ[node_id]:
        output = analyzer(spinor, orientation, P_in)
        if node_id[-1] == "1":
            dico_probability += local_computation(*output["up"], G, dico_orientation, node_id)
        if node_id[-1] == "0":
            dico_probability += local_computation(*output["down"], G, dico_orientation, node_id)

    return dico_probability

def build_json(spinor=(1,0)):
    G, dico_orientation = graph()
    dico_probability = local_computation(spinor, 1, G, dico_orientation)
    data = dico_orientation + dico_probability
    for n in G:
        if isinstance(data[n], tuple):
            G.nodes[n]["display"] = str(tuple([f"{x:.3f}" for x in data[n]]))
            G.nodes[n]["type"] = 0
        elif isinstance(data[n], float):
            if data[n] < 1e-5:
                data[n] = 0 # zero probability
            x = data[n]
            G.nodes[n]["display"] = str(f"{x:.3f}") # truncate
            G.nodes[n]["type"] = 1
    # write json formatted data
    d = nx.json_graph.node_link_data(G)  # node-link format to serialize
    # write json
    json_string = json.dumps(d)
    print(json_string)
    return json_string

theta = float(js.document.querySelector("#theta-selector").children[1].value) * np.pi
phi = float(js.document.querySelector("#phi-selector").children[1].value) * np.pi
json_string = build_json(spinor(theta, phi))