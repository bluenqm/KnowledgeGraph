# from text_extractor import TextExtractor
#
# mdpi_downloaded_folder = "D:/Working/NACTEM/BAE/Code/KnowledgeGraph/MDPI"
# mdpi_extracted_csv_file = "../../Data/mdpi_sentences.csv"
# text_extractor = TextExtractor(mdpi_downloaded_folder, mdpi_extracted_csv_file)
# text_extractor.extract_text_in_downloaded_folder()
from neo4j_adder import Neo4JAdder

n4j = Neo4JAdder()
n4j.bulk_add_relation()