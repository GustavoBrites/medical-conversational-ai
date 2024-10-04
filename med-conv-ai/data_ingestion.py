import pandas as pd
import minsearch

def load_index(DATA_PATH="../data/qa_data.csv"):
    
    df = pd.read_csv(DATA_PATH)

    documents = df.to_dict(orient='records')

    index = minsearch.Index(
        text_fields=[ 
                        'question_type',
                        'question'
                        'answer'],
        keyword_fields=["id"]
    ) 

    index.fit(documents) 
    return index