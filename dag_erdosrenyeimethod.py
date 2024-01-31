#Code by Fatima F Raadia - creating dags using the erdos_renyi_graph method

import networkx as nx
import random
import matplotlib.pyplot as plt

def erdos_renyi_dag(n, p):
    # Step 1: Use Erdos-Renyi approach to generate undirected edges
    graph = nx.erdos_renyi_graph(n, p)
    
    # Step 2: Arbitrarily order the vertices
    vertices = list(graph.nodes())
    random.shuffle(vertices)
    print('Vertices are: ', vertices)

    # Step 3: Forming a DAG from the graph
    dag = nx.DiGraph()

    # Randomly choose q values for d=0 and d=1
    q_d0 = random.randint(0, 6)
    q_d1 = random.randint(0, 6)
    
    # Adding nodes to the empty dag with properties
    for v in vertices:
        d_value = random.choice([0, 1])
        q_value = q_d0 if d_value == 0 else q_d1
        dag.add_node(v, c=random.randint(1, 8), q=q_value, d=d_value)
    print('length of V = ', len(vertices))
    
    #Assigning direction to edges
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            if graph.has_edge(vertices[i], vertices[j]):
                dag.add_edge(vertices[i], vertices[j])
                #print('edge added: ', vertices[i], '-->' ,vertices[j])
    return dag

def identify_no_incoming_outgoing(dag):
    # Step 1: Identify vertices with no incoming edges
    V_noIncoming = [v for v in dag.nodes() if not any(dag.in_edges(v))]
    #print('the nodes with no incoming edges are: ', V_noIncoming)
    
    # Step 2: Identify vertices with no outgoing edges
    V_noOutgoing = [v for v in dag.nodes() if not any(dag.out_edges(v))]
    #print('the nodes with no outgoing edges are: ', V_noOutgoing)
    return V_noIncoming, V_noOutgoing

def add_dummy_nodes(dag, V_noIncoming, V_noOutgoing):
    # Default values for dummy nodes
    dummy_source = 'None'
    dummy_sink = 'None'

    # Step 3: If |V_noIncoming| > 1, create a new dummy source node
    if len(V_noIncoming) >= 1:
        dummy_source = 'dummy_source'
        dag.add_node(dummy_source,c=0, q=0, d=-1)
        for v in V_noIncoming:
            dag.add_edge(dummy_source, v)
            
    # Step 4: If |V_noOutgoing| > 1, create a new dummy sink node
    if len(V_noOutgoing) >= 1:
        dummy_sink = 'dummy_sink'
        dag.add_node(dummy_sink,c=0, q=0, d=-2)
        for v in V_noOutgoing:
            dag.add_edge(v, dummy_sink)
            
    return dummy_source, dummy_sink


def save_dag_info_to_file(dag, V_noIncoming, V_noOutgoing, file_path):
    with open(file_path, 'w') as file:
        file.write("Edges:\n")
        for edge in dag.edges():
            file.write(f"{edge[0]} -> {edge[1]}\n")

        file.write("\nVertices with no incoming edges (V_noIncoming):\n")
        file.write(', '.join(map(str, V_noIncoming)))
        file.write("\nVertices with no outgoing edges (V_noOutgoing):\n")
        file.write(', '.join(map(str, V_noOutgoing)))

        # Accessing properties of a node in DAG
        for node, data in dag.nodes(data=True):
            file.write(f"\nNode: {node}: {data}")

# Visualize the DAG
def dagImageSave(dag, filename):
    
    plt.figure(figsize=(10,10))
    # Set node colors based on the value of d
    node_colors = ['darkslategray' if dag.nodes[node]['d'] == -2 else 'slategray' if dag.nodes[node]['d'] == -1 else 'lightcoral' if dag.nodes[node]['d'] == 0 else 'skyblue' for node in dag.nodes]
    labels = {node: f"{node}\n(c={dag.nodes[node]['c']}, q={dag.nodes[node]['q']}, d={dag.nodes[node]['d']})" for node in dag.nodes}
    # Set font size for labels
    font_size = 8

    nx.draw(dag, with_labels=True, labels=labels, node_color=node_colors, font_size=font_size)
    
    #filename = os.path.join(save_dir, f"DAG_Task_{node}.png")
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1)

    #plt.show()


def generateDAG(num_vertices, probability, output_file_path, image_file_path):
    dag = erdos_renyi_dag(num_vertices, probability)
    V_noIncoming, V_noOutgoing = identify_no_incoming_outgoing(dag)
    dummy_source, dummy_sink = add_dummy_nodes(dag, V_noIncoming, V_noOutgoing)
    save_dag_info_to_file(dag, V_noIncoming, V_noOutgoing, output_file_path)
    dagImageSave(dag, image_file_path)

    return dag


# Example usage:
num_vertices = 5
probability = 0.3
output_file_path = 'dag_info.txt'

dag = generateDAG(num_vertices,probability)

# Visualize the DAG
nx.draw(dag, with_labels=True, font_weight='bold')
plt.show()
