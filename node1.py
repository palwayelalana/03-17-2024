import os
import openai
import networkx as nx
import matplotlib.pyplot as plt
from glob import glob
import json

# Set your OpenAI API key directly in the script
# It's a placeholder; you should replace 'YOUR_API_KEY_HERE' with your actual OpenAI API key.
openai.api_key = 'api-key'

def create_graph_from_response(response):
    # Initialize an empty directed graph
    G = nx.DiGraph()

    # Process the response line by line
    for line in response.split('\n'):
        if "->" in line:
            parts = line.split("->")
            source = parts[0].strip()
            target = parts[1].strip().rstrip(";")
            G.add_edge(source, target)

    return G

def generate_knowledge_graph(cpp_code):
    # Craft a prompt for analyzing C++ code
    prompt = (
        "Please analyze the following C++ code and generate a knowledge graph.\n\n"
        "Code:\n" + cpp_code + "\n\n"
        "List the relationships in the code as edges in the following format:\n"
        "ClassA -> ClassB;\nFunctionX -> VariableY;\n"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant who can analyze C++ code."},
            {"role": "user", "content": prompt}
        ]
    )

    structured_response = response.choices[0].message['content']

    graph = create_graph_from_response(structured_response)
    return graph

def update_knowledge_graph(directory_path):
    file_paths = glob(os.path.join(directory_path, '**', '*.cc'), recursive=True) + \
                 glob(os.path.join(directory_path, '**', '*.hh'), recursive=True)

    global_graph = nx.DiGraph()

    for file_path in file_paths:
        print(file_path)
        with open(file_path, 'r') as file:
            cpp_code = file.read()
            file_graph = generate_knowledge_graph(cpp_code)
            global_graph = nx.compose(global_graph, file_graph)

    return global_graph

directory_path = 'F:\Research NCSU\gem5-stable\src\cpu\o3'  # Replace with your directory path
knowledge_graph = update_knowledge_graph(directory_path)

plt.figure(figsize=(12, 12))
pos = nx.spring_layout(knowledge_graph)
nx.draw(knowledge_graph, pos, with_labels=True, arrows=True)
plt.show()


