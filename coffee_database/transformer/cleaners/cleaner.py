
import pandas as pd
import os,re,json,sys
from tqdm import tqdm
from dotenv import load_dotenv
from sqlalchemy import create_engine
from attribute_cleaner.price_cleaner import price_cleaner
from attribute_cleaner.general_string_cleaner import text_cleaner
from attribute_cleaner.altitude_cleaner import extract_altitude
from attribute_cleaner.roast_level import get_roast_level
from datetime import datetime
import sqlalchemy
import spacy
from sqlalchemy.types import VARCHAR,TIMESTAMP,BIGINT,NUMERIC,BOOLEAN,DATE,TEXT
from sqlalchemy.dialects.postgresql import JSONB

import warnings
# Suppress all warnings
warnings.filterwarnings("ignore")

load_dotenv()

roaster_list = ['savorworks','bloom_coffee_roasters','blue_tokai','corridor_seven','curious_life','greysoul',
                'kapi_kottai','kc_roasters','koffie_genetics','naivo','quick_brown_fox'
                ]

# List of standard cols
standard_cols = ["roaster","name", "link", "price", "altitude", "varietal", "processing", 
                "estate", "roast_level", "tasting_notes", "description", 
                "country", "scraped_at","transformed_at","extra_properties","ner_properties"]

# Create an SQLAlchemy engine (replace with your actual database URL)
engine = sqlalchemy.create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')

nlp = spacy.load('/Users/snehil/Work/self/coffee/coffee_database/ner/output_try_3/model-best/')

def return_each_label(text):
    return_dict = {}
    final_dict = {}

    if text:
        doc = nlp(text.lower())
        
        for ent in doc.ents:
            # print(ent.label_)
            if ent.label_ not in return_dict.keys():
                return_dict[ent.label_] = [ent.text]
            else:
                return_dict[ent.label_].append(ent.text)

        for key,val in return_dict.items():
            final_dict[key] = ' , '.join(list(set(return_dict[key]))) if return_dict[key] else None
    return final_dict

for roaster in tqdm(roaster_list, desc="Processing roasters"):

    # Define your SQL query
    query = f"""
    select * from raw_scraped.{roaster}
    """
    
    df = pd.read_sql(query, con=engine)
    df.columns = [re.sub(r'[^\w]+', '_', i.lower()).strip('_') for i in df.columns]

    if roaster=='blue_tokai':
        df.rename(columns={'tasting_notes':'bt_tasting_notes'},inplace=True)

    df.rename(columns={'origin': 'estate',
                    'process': 'processing',
                    'elevation': 'altitude',
                    'roast': 'roast_level',
                    'flavor': 'tasting_notes',
                    'tastes_like': 'tasting_notes',
                    'roasting_profile': 'roast_level',
                    'estate_name': 'estate',
                    'roast_profile': 'roast_level',
                    'roaster_thoughts': 'description',
                    'product_name': 'name',
                    'url': 'link',
                    'name_of_coffee': 'name',
                    'varieties': 'varietal',
                    'flavor_notes': 'tasting_notes',
                    }, inplace=True)

    columns_missing_from_standard_table = [i for i in standard_cols if i not in df.columns.tolist()]
    df[columns_missing_from_standard_table] = None

    col_text_cleaner = ['estate','varietal','processing','tasting_notes','acidity','body','aftertaste','description','variety']
    for text_col in col_text_cleaner:
        try:
            df[text_col] = df[text_col].apply(text_cleaner)
        except KeyError:
            pass

    if 'variety' in df.columns:
        df['varietal'] = df['varietal'].where(df['varietal'].notna(), df['variety'])
        df.drop(['variety'],inplace=True,axis=1)
    if 'bt_tasting_notes' in df.columns:
        df['tasting_notes'] = df['tasting_notes'].where(df['tasting_notes'].notna(), df['bt_tasting_notes'])
        df.drop(['bt_tasting_notes'],inplace=True,axis=1)


    df["extra_properties"] = df.apply(lambda row: {col: row[col] for col in df.columns if col not in standard_cols}, axis=1)
    df['extra_properties'] = df['extra_properties'].apply(json.dumps)

    df["ner_properties"] = df['description'].apply(return_each_label)
    df["ner_properties"] = df["ner_properties"].apply(json.dumps)

    # taking missing cols from NER dict
    # TYPE CODE HERE to extract missing fields from NER 

    # taking care of extra or less columns
    df = df[standard_cols]  

    idx = df.groupby('name')['scraped_at'].idxmax()
    df = df.loc[idx]
    df.reset_index(drop=True,inplace=True)
    df["roaster"] = roaster 
    df['price'] = df.price.apply(price_cleaner)
    df['altitude'] = df.altitude.apply(extract_altitude)
    df['roast_level'] = df.apply(lambda row: get_roast_level(row['roast_level'], row['description']), axis=1)
    
    df['country'] = df['country'].where(df['country'].notna(), 'india')
    df['transformed_at'] = datetime.now()    

    # print(df.columns)
    # df = df[standard_cols + ["extra_properties"]]
    # df = df[standard_cols + ["ner_properties"]]

    # type_col = {col_name: TEXT for col_name in df}

    # type_col['transformed_at'] = TIMESTAMP
    # type_col['scraped_at'] = TIMESTAMP
    # type_col['extra_properties'] = JSONB
    # type_col['ner_properties'] = JSONB



    # putting it into db
    conn = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
    # df.to_sql(name = 'transformed_stg' , con=conn, index=False, if_exists='append',dtype=type_col,schema='public')
    df.to_sql(name = 'transformed_stg' , con=conn, index=False, if_exists='append',schema='public')

    print(f'{roaster} TRANSFORMED !!!')
    



