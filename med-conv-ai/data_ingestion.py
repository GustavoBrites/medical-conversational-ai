import pandas as pd
import minsearch
import os

DATA_PATH = os.getenv("DATA_PATH", "../data/qa_data.csv")

# def load_index(DATA_PATH="data/qa_data.csv"):
def load_index():

    df = pd.read_csv(DATA_PATH)

    documents = df.to_dict(orient='records')

    index = minsearch.Index(
        text_fields=[ 
                        'question_type',
                        'question',
                        'answer'],
        keyword_fields=["id"]
    ) 

    index.fit(documents) 
    return index

print("here")