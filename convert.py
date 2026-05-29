# Convert the project list to a .json file

import pandas as pd
import numpy as np
import json
import re

# easier to use helper functions instead of lambdas
def parse_csv_list(val): # for tags / intended environments where the value is a list
    if pd.isna(val): 
        return []
    return sorted([item.strip() for item in str(val).split(',') if item.strip()]) # sort alphabetically just in case

def safe_int(val): # helper function to handle missing values
    if pd.isna(val): 
        return None
    match = re.search(r'(\d{4})', str(val))
    return int(match.group(1)) if match else None

df = pd.read_excel('./Project List.xlsx') # excel reading is inbuilt to pandas (yay!)
dfo = pd.DataFrame() # create output dataframe 

dfo['id'] = df['ID'].astype(int)
dfo['shortName'] = df['ShortN'].astype(str).str.strip()
dfo['longName'] = df['Project Name (Long)'].astype(str).str.strip()
dfo['startYear'] = df['Year Started'].apply(safe_int)
dfo['lastActive'] = df['Last Active'].apply(safe_int)
dfo['department'] = df['Department'].astype(str).str.strip()
dfo['isCompleted'] = df['Completed?'].astype(str).str.strip().str.lower().isin(['yes', 'true', 'y', '1'])
dfo['designEnv'] = df['Designed For?'].apply(parse_csv_list)
dfo['tags'] = df['Tags'].apply(parse_csv_list)
dfo['description'] = df['Description'].astype(str).str.strip()
dfo['imageUrl'] = df['Image URL'].astype(str).str.strip().replace({'nan': None, '': None})

# Convert to list of dicts & clean pandas NaN types for JSON
records = dfo.replace({np.nan: None}).to_dict(orient='records')

with open('./projects.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, indent=1, ensure_ascii=False)
