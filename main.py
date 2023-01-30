import pandas
from KnowledgeGraphGenerator import KnowledgeGraphGenerator

candidate_sentences_dataframe = pandas.read_csv("../../Data/wiki_sentences_v2.csv")
kgg = KnowledgeGraphGenerator(candidate_sentences_dataframe, "../../Data/relations.csv")
kgg.display_relation("released in")