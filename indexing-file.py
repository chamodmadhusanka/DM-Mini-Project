# -*- coding: utf-8 -*-
"""metaphorica.ipynb
Original file is located at
    https://colab.research.google.com/drive/1fJk3xB9AP4O99m_q6VXxjKc6u0ebKdQ1
"""

import pandas as pd
from elasticsearch import Elasticsearch

poem_corpus_csv_path = '/Dataset/corpus.csv'
poem_corpus_df = pd.read_csv(poem_corpus_csv_path)

poem_corpus_df.shape

poem_corpus_df.head()

"""## Connect to elasticsearch"""

ENDPOINT = ""  # add running elasticsearch URL here
USERNAME = ""
PASSWORD = ""

es = Elasticsearch(hosts=[ENDPOINT], http_auth=(USERNAME, PASSWORD), timeout=300)

es.ping()

"""## Create index"""

# PUT posting
config = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "poem_name": {
                "type": "text"
            },
            "poet": {
                "type": "text",
            },
            "line": {
                "type": "text"
            },
            "metaphor_present": {
                "type": "text"
            },
            "metaphor_count": {
                "type": "text"
            },
            "metaphorical_terms": {
                "type": "text"
            },
        }
    }
}

es.indices.create(
    index="poem",
    settings=config["settings"],
    mappings=config["mappings"],
)

"""## Insert data to elasticsearch"""

# Fill all potential None or NaN values with empty strings
poem_corpus_df.fillna("", inplace=True)

for i, row in poem_corpus_df.iterrows():

    try:
        doc = {
            "poem_name": row["Poem Name"],
            "poet": row["Poet"],
            "line": row["Line"],
            "metaphor_present": row["Metaphor present or not"],
            "metaphor_count": row["Count of the metaphor"],
            "metaphorical_terms": str(row["Metaphorical terms"]),
        }
        es.index(index="poem", id=i, document=doc)
    except Exception as e:
        print(print(f"An error occurred: {e}"))
        pass
