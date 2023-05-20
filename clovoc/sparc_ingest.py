import os
import requests

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from requests_helper import http_status_to_message, PhenoNode

def get_hpo_search_results(hpo_term: str):
    token = os.environ.get('SCI_CRUNCH_API_KEY0')

    phenotype_url = f'https://scicrunch.org/api/1/sckan-scigraph/dynamic/prod/sparc/phenotypeAnatomy/{hpo_term}?key={token}'

    with requests.Session() as session:
        response = session.get(phenotype_url)
    
    return response


def build_relationship_graph_for_hpo_term(hpo_term: str):

    response = get_hpo_search_results(hpo_term=hpo_term)
    
    print(http_status_to_message(response.status_code))

    pheno_graph = nx.Graph()
    node_map = {}

    for top_level in response.json():
        if top_level == 'nodes':
            for node in response.json()['nodes']:
                if node['id']:
                    pheno_node = PhenoNode(uberon=node['id'],name=node['lbl'])
                    node_map.setdefault(node['id'],pheno_node)
                    pheno_graph.add_node(pheno_node)
        if top_level == 'edges':
            for edge in response.json()['edges']:
                if edge['sub'] and edge['obj'] and edge['sub'] != edge['obj']:
                    pheno_graph.add_edge(node_map[edge['sub']],node_map[edge['obj']])  
            
    nx.draw(pheno_graph, with_labels=True)

    plt.show()

def get_searchable_hpos():
    cwd = os.getcwd() if 'clovoc' in os.getcwd() else os.path.join(os.getcwd(),'clovoc')
    hpo_df = pd.read_csv(f'{cwd}/' + 'clovoc_hpo_table.csv')
    hpo_df = hpo_df[[col for col in hpo_df.columns if col.startswith('Condition') or col.startswith('Body')]]
    hpo_df = hpo_df[['Condition Code','Condition Name']].set_index('Condition Code')
    return hpo_df.to_dict()

def check_query_terms(hpos: list):
    for hpo in hpos:
        response = get_hpo_search_results(hpo)
        if http_status_to_message(response.status_code) == 'OK':
            print(f'{hpo} found')
        else:
            print(f'{hpo} not found')

print('Searchable hpos:')
hpos = get_searchable_hpos()['Condition Name']
for index, label in hpos.items():
    print(f'{index}: {label}')

while (user_input := input("Which hpo would you like a graph for? ")):
    build_relationship_graph_for_hpo_term(user_input)