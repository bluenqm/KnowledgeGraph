from bs4 import BeautifulSoup
import csv
import spacy
nlp = spacy.load("en_core_web_sm")
import os
from tqdm import tqdm
import pandas as pd

class TextExtractor:
    def __init__(self, downloaded_folder, csv_filename):
        self.csv_filename = csv_filename
        self.downloaded_folder = downloaded_folder
        self.results = pd.DataFrame(columns=['sentence'])

    def extract_text_in_downloaded_folder(self):
        for filename in tqdm(os.listdir(self.downloaded_folder)):
            full_file_name = os.path.join(self.downloaded_folder, filename)
            if os.path.isfile(full_file_name):
                self.extract_text(full_file_name)
        self.write_to_csv_file()
    def extract_text(self, html_file):
        with open(html_file, "r", encoding="UTF-8") as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.find("div", class_="html-p").get_text()
        text = '\n'.join([line for line in text.splitlines() if line.strip()])
        doc = nlp(text)
        for sentence in doc.sents:
            text_to_write = sentence.text.strip()
            if len(text_to_write) >= 20:
                self.results = pd.concat([
                    self.results,
                    pd.DataFrame({'sentence': [text_to_write]})
                ])
    def write_to_csv_file(self):
        if os.path.exists(self.csv_filename):
            os.remove(self.csv_filename)
        self.results.to_csv(self.csv_filename)

