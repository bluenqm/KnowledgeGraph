import os
import pandas
from spacy.matcher import Matcher
import spacy
nlp = spacy.load("en_core_web_sm")
from tqdm import tqdm
import networkx
import matplotlib.pyplot as plt

class KnowledgeGraphGenerator:
    def __init__(self, candidate_sentences_dataframe, knowledge_graph_dataframe_location):
        self.candidate_sentences_dataframe = candidate_sentences_dataframe
        self.knowledge_graph_dataframe_location = knowledge_graph_dataframe_location
        if not os.path.exists(knowledge_graph_dataframe_location):
            self.generate_knowledge_graph()

    def get_entities(self, sentence):
        entity_1 = ""
        entity_2 = ""
        previous_token_dependency_tag = ""
        previous_token_text = ""
        prefix = ""
        modifier = ""

        for token in nlp(sentence):
            if token.dep_ == "punct":
                continue
            if token.dep_ == "compound":
                if previous_token_dependency_tag == "compound":
                    prefix = previous_token_text + " " + token.text
                else:
                    prefix = token.text
            if token.dep_.endswith("mod") == True:
                if previous_token_dependency_tag == "compound":
                    modifier = previous_token_text + " " + token.text
                else:
                    modifier = token.text
            if token.dep_.find("subj") == True:
                entity_1 = modifier + " " + prefix + " " + token.text
                prefix = ""
                modifier = ""
            if token.dep_.find("obj") == True:
                entity_2 = modifier + " " + prefix + " " + token.text
                prefix = ""
                modifier = ""
            previous_token_dependency_tag = token.dep_
            previous_token_text = token.text

        return [entity_1.strip(), entity_2.strip()]

    def get_relation(self, sentence):
        doc = nlp(sentence)
        matcher = Matcher(nlp.vocab)
        pattern = [
            [{'DEP': 'ROOT'}, {'DEP': 'prep', 'OP': "?"}, {'DEP': 'agent', 'OP': "?"}],
            [{'POS': 'ADJ', 'OP': "?"}]
        ]
        matcher.add("MATCHING", patterns=pattern)
        matches = matcher(doc)
        k = len(matches) - 1
        span = doc[matches[k][1]:matches[k][2]]
        return (span.text)

    def generate_knowledge_graph(self):
        entity_pairs = []
        for i in tqdm(self.candidate_sentences_dataframe["sentence"]):
            entity_pairs.append(self.get_entities(i))
        subjects = [i[0] for i in entity_pairs]
        objects = [i[1] for i in entity_pairs]

        relations = []
        for i in tqdm(self.candidate_sentences_dataframe['sentence']):
            relations.append(self.get_relation(i))
        knowledge_graph_dataframe = pandas.DataFrame({'source': subjects, 'target': objects, 'edge': relations})
        knowledge_graph_dataframe.to_csv(self.knowledge_graph_dataframe_location)

    def display_relation(self, relation_text):
        kg_df = pandas.read_csv(self.knowledge_graph_dataframe_location)
        G = networkx.from_pandas_edgelist(kg_df[kg_df['edge'] == relation_text],
                                          "source",
                                          "target",
                                          edge_attr=True,
                                          create_using=networkx.MultiDiGraph())

        plt.figure(figsize=(12, 12))
        pos = networkx.spring_layout(G, k=0.5)  # k regulates the distance between nodes
        networkx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, pos=pos)
        plt.show()