from data_cleaning import clean_df
import pandas as pd
import json
from keybert import KeyBERT
"""
Returns dataframe with extracted keywords
"""

with open ('06_text_df.json',encoding='utf-8') as f:
    data = json.load(f)

# writing the json data into a dataframe
df_json = pd.json_normalize(data, record_path =['PDF'])

end_result = clean_df(df_json)


def listAppender(textListInput):
    """
    Returns combined string from given strings.
    """
    return " ".join(textListInput)

def keybert_ext(df = pd.DataFrame):
    """
    Returns dataframe with extracted keywords
    """
    kw_model = KeyBERT('paraphrase-MiniLM-L6-v2')
    englishDf =  df.loc[df["file_language"] == "English"]
    englishDf = englishDf.reset_index()
    englishDf["extracted_keywords"] = None
    englishDf["text_clean"] = englishDf["text_clean"].apply(listAppender)
    text_clean_list = englishDf["text_clean"].tolist()
    extracted_keywords = kw_model.extract_keywords(text_clean_list, keyphrase_ngram_range=(1, 2), top_n=5)
    englishDf["extracted_keywords"] = extracted_keywords

    return englishDf

print(keybert_ext(end_result)["extracted_keywords"])