import os

from py2neo import Graph, Node, Relationship
from tqdm import tqdm
import json

class Neo4JAdder:
    def __init__(self, uri="bolt://127.0.0.1", user="neo4j", password="NaCTeM2023"):
        self.graph = Graph(uri, auth=(user, password))

    def add_relation(self, relation, head_span_text, head_span_id, tail_span_text, tail_span_id):
        if head_span_id == 'id-less':
            head_span_id = head_span_text
        if tail_span_id == 'id-less':
            tail_span_id = tail_span_text
        if head_span_text == tail_span_text and head_span_id == tail_span_id:
            return
        h = Node("ENTITY", name=head_span_text, id=head_span_id)
        t = Node("ENTITY", name=tail_span_text, id=tail_span_id)
        self.graph.merge(h, "ENTITY", "id")
        self.graph.merge(t, "ENTITY", "id")
        h_rel_t = Relationship(h, relation, t)
        self.graph.merge(h_rel_t)

    def bulk_add_relation(self, dir="D:/Working/NACTEM/BAE/Code/KnowledgeGraph/Relations"):
        for filename in tqdm(os.listdir(dir)):
            full_file_name = os.path.join(dir, filename)
            if not os.path.isfile(full_file_name):
                continue
            with open(full_file_name, "r", encoding="UTF-8") as file:
                lines = file.readlines()
                for line in lines:
                    relation, head_span_text, head_span_id, tail_span_text, tail_span_id = self.get_relationships(line)
                    if relation != "":
                        self.add_relation(relation, head_span_text, head_span_id, tail_span_text, tail_span_id)

    def get_relationships(self, line):
        # 0:{'relation': 'use', 'head_span': {'text': 'numerical prediction', 'id': 'Q112890715'}, 'tail_span': {'text': 'performance', 'id': 'Q35140'}}
        text = line.replace("\'", "\"")
        json_str = text.split(':', 1)[1]
        try:
            data = json.loads(json_str)
            relation = data['relation']
            head_span_text = data['head_span']['text']
            head_span_id = data['head_span']['id']
            tail_span_text = data['tail_span']['text']
            tail_span_id = data['tail_span']['id']
            return relation, head_span_text, head_span_id, tail_span_text, tail_span_id
        except:
            return "", "", "", "", ""
