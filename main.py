import pandas
from knowledge_graph_generator import KnowledgeGraphGenerator
from mdpi_web_crawler import MDPIWebCrawler

#candidate_sentences_dataframe = pandas.read_csv("../../Data/wiki_sentences_v2.csv")
#kgg = KnowledgeGraphGenerator(candidate_sentences_dataframe, "../../Data/relations.csv")
#kgg.display_relation("released in")

mdpi_web_crawler = MDPIWebCrawler()
mdpi_web_crawler.crawl()