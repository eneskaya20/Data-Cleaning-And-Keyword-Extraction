import json
import pandas as pd
import re
import unicodedata

pd.set_option('display.max_colwidth', None)

def load_json_file(file_path):
    """
    Returns json file 
    """    
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    return data

# load json file to a dataframe
data = load_json_file('06_text_df.json')
df_json = pd.json_normalize(data, record_path=['PDF'])

def remove_broken(text):
    """
    Returns text without broken characters
    """    
    result = re.sub(r'^.*' + re.escape("ARABIN GULF MINE ACTION.CO") + r'.*$', ' ', text, re.MULTILINE)

    return result

def normalize_dot(text):
    """
    Returns text with normalized dots
    """
    tmp = re.sub(r'•+', '*', text)
    tmp = re.sub(r'·+', '*', tmp)
    result = re.sub(r'●+', '*', tmp)

    return result

def normalize_dash(text):
    """
    Returns text with normalized dashes
    """
    tmp = text.replace('‐', '-') #invalid character '‐' (U+2010)
    tmp = tmp.replace('‑', '-') #invalid character '‑' (U+2011)
    tmp = tmp.replace('‒', '-') #invalid character '‒' (U+2012)
    tmp = tmp.replace('—', '-') #invalid character '‐' (U+2014)
    result = tmp.replace('–', '-') #invalid character '–' (U+2013)

    return result

def normalize_quotation(text):
    """
    Returns text with normalized quotation marks
    """
    tmp = text.replace('“', '"') #invalid character '“' (U+201C)
    tmp = tmp.replace('„', '"')
    tmp = tmp.replace('‟', '"')
    result = tmp.replace('”', '"') #invalid character '”' (U+201D)

    return result

def normalize_apostrophe(text):
    """
    Returns text with normalized apostrophes
    """
    tmp = text.replace('‘', "'") #invalid character '‘' (U+2018)
    tmp = tmp.replace("´", "'") #invalid character '´' (U+00B4)
    result = tmp.replace('’', "'") #invalid character '’' (U+2019)

    return result

def normalize_brackets(text):
    """
    Returns text with normalized brackets
    """
    tmp = text.replace('（', '(') #invalid character ' (' (U+FF08)
    result = tmp.replace('）', ')') #invalid character '）' (U+FF09)

    return result

def remove_nonprintable(text):
    """
    Returns text without non-printable characters
    """
    tmp = text.replace("　", " ")# invalid non-printable character U+3000
    tmp = tmp.replace("", " ")
    tmp = tmp.replace('★', "*")
    tmp = tmp.replace(' ', ' ') #invalid character ' ' (U+00a0)
    tmp = tmp.replace(u'\xa0', " ")
    tmp = tmp.replace("：", ":")
    tmp = tmp.replace("！", "!")
    result = tmp.replace("�", " ")

    return result

def is_pua(c):
    return unicodedata.category(c) == 'Co'

def remove_pua(text):
    """
    Returns text without private use area characters
    """
    result = "".join(c for c in text if not is_pua(c)) # for characters like \uf0b7

    return result

def normalize_new_line(text):
    """
    Returns text with normalized new lines
    """
    result = re.sub(r'\r{1,}', '\n', text)

    return result

def replace_excessive_commas(text):
    """
    Returns text with normalized commas
    """
    result = re.sub(r"\,{2,}", ",", text) 

    return result

def replace_excessive_dots(text):
    """
    Returns text with normalized dots
    """
    tmp = re.sub(r"(\…\s*){1,}", ".", text)
    result = re.sub(r"(\.\s*){2,}", ".", tmp)

    return result

def replace_excessive_stars(text):
    """
    Returns text with normalized stars
    """
    result = re.sub(r"(\*\s*){3,}", "*", text)

    return result

def replace_excessive_lines(text):
    """
    Returns text with normalized lines
    """
    result = re.sub(r"\-{4,}", "-", text)

    return result

def remove_dates(text):
    """
    Returns text without dates
    """
    result = re.sub(r'\[\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}\]', " [DATE]", text) 

    return result

def replace_URLs(text):
    """
    Returns text without URLs
    """
    result = re.sub(r"http[s]?://\S+", "[URL]", text) 

    return result

def remove_excessive_spaces(text):
    """
    Returns text without excessive spaces
    """
    result = re.sub(r"\s{2,}", " ", text) 

    return result

def remove_extra_spaces(text):
    """
    Returns text without extra spaces
    """
    result = re.sub(r"^\s+|\s+$", "", text) 

    return result

def clean_text(text_list):
    """
    Returns cleaned text
    """
    out = []
    for text in text_list:
        tmp = normalize_dot(text)
        tmp = remove_broken(tmp)
        tmp = normalize_dash(tmp)
        tmp = normalize_quotation(tmp)
        tmp = normalize_apostrophe(tmp)
        tmp = normalize_brackets(tmp)
        tmp = remove_nonprintable(tmp)
        tmp = remove_pua(tmp)
        tmp = normalize_new_line(tmp)
        tmp = replace_excessive_commas(tmp)
        tmp = replace_excessive_dots(tmp)
        tmp = replace_excessive_lines(tmp)
        tmp = replace_excessive_stars(tmp)
        tmp = remove_dates(tmp)
        tmp = replace_URLs(tmp)
        tmp = remove_excessive_spaces(tmp)
        tmp = remove_extra_spaces(tmp)
        
        out.append(tmp)

    return out

def clean_df(df):
    """
    Returns dataframe with cleaned text
    """
    df['text_clean'] = df['file_text'].apply(clean_text)
    return df

end_result = clean_df(df_json)





